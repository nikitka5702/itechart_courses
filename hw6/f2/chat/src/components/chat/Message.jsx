import React from 'react'

function Message(props) {
  return (
    <div className="card">
      <h5 className="card-title">{props.author}</h5>
      <h6 className="card-subtitle mb-2 text-muted">{props.posted_at}</h6>
      <p className="card-text">{props.text}</p>
    </div>
  )
}

export default Message
