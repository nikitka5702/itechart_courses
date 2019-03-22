import React, { Component } from 'react'

import axios from 'axios'

class Admin extends Component {
  render() {
    return (
      <div className="row">
        <div className="col">
          <div className="card">
            <table className="table table-striped">
              <thead>
                <tr>
                  <th scope="col">Chat ID</th>
                  <th scope="col" colSpan="2">Actions</th>
                </tr>
              </thead>
              <tbody>
                {Array.apply(0, Array(10)).map(
                  function (val, i) { 
                    return (
                      <tr key={i}>
                        <th scope="row">{i + 1}</th>
                        <td>
                          <button className="btn btn-warning" onClick={
                            (e) => {
                              e.preventDefault()
                              axios.post(
                                `http://localhost:8000/admin/logout/${i}`
                              ).then((resp) => console.log(resp.data))
                            }
                          }>Logout Users</button>
                        </td>
                        <td>
                          <button className="btn btn-danger" onClick={
                            (e) => {
                              e.preventDefault()
                              axios.post(
                                `http://localhost:8000/admin/purge/${i}`
                              ).then((resp) => console.log(resp.data))
                            }
                          }>Purge</button>
                        </td>
                      </tr>
                    ) 
                  }
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    )
  }
}

export default Admin
