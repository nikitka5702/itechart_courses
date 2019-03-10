import logging

from tornado.web import RequestHandler, Application, url
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler
from tornado.locks import Condition
from tornado.escape import json_decode, json_encode
from tornado.options import define, options, parse_command_line

from models import User, Message, Session


define('port', default=8000, help="run on the given port", type=int)


rooms = [[] for _ in range(10)]

session = Session()


class ChatSocketHandler(WebSocketHandler):
    waiters = set()

    def check_origin(self, origin):
        return True

    def open(self, username, room):
        room = int(room)
        u = User(username=username, room=room)
        session.add(u)
        session.commit()
        rooms[room].append((u, self))
        self.user = u
        print(f'Created user {u}')
        q = session.query(Message).filter(Message.room == room).order_by(Message.posted_at).all()
        ChatSocketHandler.waiters.add(self)
        self.write_message(json_encode({'initial': True, 'messages': [x.to_dict() for x in q]}))
        UserSocketHandler.send_users()

    def on_close(self):
        rooms[self.user.room].remove((self.user, self))
        ChatSocketHandler.waiters.remove(self)
        UserSocketHandler.send_users()
    
    def on_message(self, msg):
        message = Message(user_id=self.user.id, text=msg, room=self.user.room)
        session.add(message)
        session.commit()
        print(message.to_dict())
        ChatSocketHandler.broadcast_message(message)
    
    @classmethod
    def broadcast_message(cls, msg):
        removable = set()
        for ws in cls.waiters:
            if not ws.ws_connection or not ws.ws_connection.stream.socket:
                removable.add(ws)
            else:
                ws.write_message(json_encode(msg.to_dict()))
        for ws in removable:
            ChatSocketHandler.waiters.remove(ws)
    
    @classmethod
    def resend_history(cls, room):
        removable = set()
        q = session.query(Message).filter(Message.room == room).order_by(Message.posted_at).all()
        for ws in cls.waiters:
            if not ws.ws_connection or not ws.ws_connection.stream.socket:
                removable.add(ws)
            else:
                ws.write_message(json_encode({'initial': True, 'messages': [x.to_dict() for x in q]}))
        for ws in removable:
            ChatSocketHandler.waiters.remove(ws)


class UserSocketHandler(WebSocketHandler):
    waiters = set()
    
    def check_origin(self, origin):
        return True

    def open(self, room):
        self.room = int(room)
        UserSocketHandler.waiters.add(self)
        UserSocketHandler.send_users()
    
    @classmethod
    def send_users(cls):
        removable = set()
        for ws in cls.waiters:
            if not ws.ws_connection or not ws.ws_connection.stream.socket:
                removable.add(ws)
            else:
                ws.write_message(json_encode([x.to_dict() for x, _ in rooms[ws.room]]))
        for ws in removable:
            UserSocketHandler.waiters.remove(ws)


class AdminHandler(RequestHandler):
    def post(self, action, chat):
        chat = int(chat)
        if action == 'purge':
            session.query(Message).filter(Message.room == chat).delete()
            ChatSocketHandler.resend_history(chat)
        elif action == 'logout':
            for _, ws in rooms[chat]:
                ws.close()
            rooms[chat].clear()
            UserSocketHandler.send_users()
    
    def option(self):
        self.set_status(200)
        self.finish()


app = Application(
    [
        url(r'/chat/([^/]+)/(\d+)', ChatSocketHandler),
        url(r'/users/(\d+)', UserSocketHandler),
        url(r'/admin/([^/]+)/(\d+)', AdminHandler)
    ]
)

try:
    app.listen(options.port)
    IOLoop.current().start()
except KeyboardInterrupt:
    IOLoop.current().stop()
