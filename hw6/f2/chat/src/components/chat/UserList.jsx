import React, { Component } from 'react'

import uuid4 from 'uuid'

class UserList extends Component {
  state = {
    users: []
  }

  constructor(props) {
    super(props)

    this.socket = new WebSocket(`ws://localhost:8000/users/${this.props.room}`)

    this.socket.onmessage = (event) => {
      let data = JSON.parse(event.data)
      this.handleData(data)
    }
  }
  
  userListStyle = {
    height: '100%',
    overflow: 'hidden',
    overflowY: 'scroll'
  }

  handleData = (data) => {
    this.setState({users: data.map((user) => user.username)})
  }

  componentWillUnmount() {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.onclose = () => {}
      this.socket.close()
    }
  }

  render() {
    return (
      <div className="card" style={{height: '600px'}}>
        <div className="card-body">
          <div style={this.userListStyle}>
            {this.state.users.map((username) => <div key={uuid4()} className="card"><div className="card-text">{username}</div></div>)}
          </div>
        </div>
      </div>
    )
  }
}

export default UserList
