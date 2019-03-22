import React, { Component } from 'react'

import uuid4 from 'uuid'

import Message from './Message'

class MessageList extends Component {
  state = {
    messages: [],
    msg: ''
  }

  constructor(props) {
    super(props)
    this.socket = new WebSocket(`ws://localhost:8000/chat/${this.props.username}/${this.props.room}`)

    this.socket.onmessage = (event) => {
      let data = JSON.parse(event.data)
      if (data.initial) {
        this.setMessages(data.messages)
      } else {
        this.addMessage(data)
      }
    }
    this.socket.onclose = (event) => {
      this.props.changeChat()
    }
  }

  messageListStyle = {
    height: '100%',
    overflow: 'hidden',
    overflowY: 'scroll'
  }

  componentWillUnmount() {
    if (this.socket.readyState === WebSocket.OPEN) {
      this.socket.onclose = () => {}
      this.socket.close()
    }
  }

  onChange = (e) => this.setState({ [e.target.name]: e.target.value })

  setMessages = (messages) => this.setState({messages})

  addMessage = (message) => this.setState({messages: [...this.state.messages, message]})

  scrollToBottom = () => this.messagesEnd.scrollIntoView({ behavior: "smooth" })

  componentDidMount() {
    this.scrollToBottom()
  }

  componentDidUpdate() {
    this.scrollToBottom()
  }

  render() {
    return (
      <div className="card" style={{height: '600px'}}>
        <div className="card" style={{height: '560px'}}>
          <div id="chat" style={this.messageListStyle}>
            {this.state.messages.map((data) => <Message key={uuid4()} {...data}/>)}
            <div style={{ float:"left", clear: "both" }}
              ref={(el) => { this.messagesEnd = el }}>
            </div>
          </div>
        </div>
        <div className="card" style={{height: '40px'}}>
          <div className="row">
            <div className="col-10">
              <input name="msg" type="text" className="form-control" onChange={this.onChange} value={this.state.msg}></input>
            </div>
            <div className="col">
              <button className="btn btn-primary btn-block" onClick={(e) => {
                e.preventDefault()
                let {msg} = this.state
                this.setState({msg: ''})
                if (msg) {
                  this.socket.send(msg)
                }
              }}>Send</button>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default MessageList
