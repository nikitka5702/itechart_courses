import React, { Component } from 'react'

import Login from '../chat/Login'
import Chat from '../chat/Chat'

class Home extends Component {
  render() {
    return this.props.isChat ? <Chat {...this.props} /> : <Login changeChat={this.props.changeChat} changeAdmin={this.props.changeAdmin} />
  }
}

export default Home
