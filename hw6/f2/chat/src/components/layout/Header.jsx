import React, { Component, Fragment } from 'react'

class Header extends Component {
  render() {
    const logout = this.props.isChat ? <button className="btn btn-outline-danger" onClick={this.props.changeChat}>Logout</button> : <Fragment />
    const admin = this.props.isAdmin ? <button className="btn btn-outline-danger" onClick={this.props.changeAdmin}>Back</button> : <Fragment />

    return (
      <header>
        <nav className="navbar navbar-dark bg-dark navbar-expand-md fixed-top">
          <a className="navbar-brand" href="/">Chat</a>
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span className="fas fa-bars" />
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav mr-auto">
                <a href="/" className="nav-link">Home</a>
              </ul>
              <ul className="navbar-nav ml-auto">
                {logout}
                {admin}
              </ul>
            </div>
        </nav>
      </header>
    )
  }
}

export default Header
