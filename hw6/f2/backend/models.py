import json
from datetime import datetime
from contextlib import contextmanager

from sqlalchemy import (
    create_engine,
    Column, Integer, String, ForeignKey, DateTime
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


__all__ = [
    'session_scope',
    'Base',
    'User',
    'Message',
    'engine',
    'Session'
]


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    room = Column(Integer)

    def __repr__(self):
        return "<User(id={}, username='{}', room={})>".format(
            self.id, self.username, self.room
        )
    
    def to_dict(self):
        return {'username': self.username}


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='messages')
    text = Column(String(255))
    room = Column(Integer)
    posted_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Message(id={}, room={}, posted_at={})>".format(
            self.id, self.room, self.posted_at
        )
    
    def to_dict(self):
        return {'text': self.text, 'posted_at': self.posted_at.strftime('%d %b %Y %H:%M:%S'), 'author': self.user.username}


engine = create_engine('postgresql+psycopg2://postgres:root@localhost/test')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
