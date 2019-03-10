import React, { Component, Fragment } from 'react'

class Login extends Component {
  state = {
    username: '',
    room: '0'
  }

  onChange = (e) => this.setState({ [e.target.name]: e.target.value })

  connectToChat = (e) => {
    e.preventDefault()
    if (!this.state.username) {
      return
    }
    console.log(`${this.state.username} requests to join to room ${this.state.room}`)

    this.props.changeChat(this.state.username, this.state.room)
  }

  adminButton = (e) => {
    e.preventDefault()
    if (this.state.username === "ADMIN") {
      this.props.changeAdmin()
    }
  }

  render() {
    return (
      <Fragment>
        <div className="d-flex justify-content-center">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Chat App</h5>
              <form>
                <div className="row" style={{marginBottom: '5%'}}>
                  <div className="col-8">
                    <input type="text" className="form-control" id="username" name="username" onChange={this.onChange} />
                  </div>
                  <div className="col">
                    <select id="room" name="room" className="form-control" onChange={this.onChange}>
                      {Array.apply(0, Array(10)).map(function (val, i) { return <option key={i} value={i}>{i + 1}</option>; })}
                    </select>
                  </div>
                </div>
                <div className="row justify-content-center">
                  <div className="col">
                    <button type="submit" className="btn btn-primary btn-block" onClick={this.connectToChat}>Enter chat</button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
        <div className="d-fexl align-items-end flex-column">
          <div className="p-2"><button style={{fontSize: '2px', backgroundColor: 'white', border: '0px'}} onClick={this.adminButton}>11</button></div>
        </div>
      </Fragment>
    )
  }
}

export default Login
