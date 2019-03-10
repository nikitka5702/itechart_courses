import React, { Component } from 'react'

import UserList from './UserList'
import MessageList from './MessageList'

class Chat extends Component {
  render() {
    return (
      <div className="row">
        <div className="col-2">
          <UserList room={this.props.room} />
        </div>
        <div className="col">
          <MessageList username={this.props.username} room={this.props.room} changeChat={this.props.changeChat} />
        </div>
      </div>
    )
  }
}

export default Chat
