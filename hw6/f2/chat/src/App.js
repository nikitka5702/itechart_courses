import React, { Component } from 'react'

import 'bootstrap/dist/css/bootstrap.min.css'

import Header from './components/layout/Header'
import Home from './components/pages/Home';
import Admin from './components/pages/Admin';

class App extends Component {
  state = {
    isChat: false,
    isAdmin: false,
    username: '',
    room: '0'
  }

  changeChat = (username, room) => {
    this.setState({isChat: !this.state.isChat, username, room})
  }

  changeAdmin = () => this.setState({isAdmin: !this.state.isAdmin})

  render() {
    const {isAdmin} = this.state

    const main = isAdmin ? <Admin /> : <Home changeChat={this.changeChat} changeAdmin={this.changeAdmin} {...this.state} />

    return (
      <div className="App">
        <Header changeChat={this.changeChat} changeAdmin={this.changeAdmin} {...this.state} />
        <div className="container">
          {main}
        </div>
      </div>
    );
  }
}

export default App
