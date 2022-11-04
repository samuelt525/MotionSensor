import React, { useState, useEffect } from 'react'
import UploadVideo from './components/UploadVideo'
import './styles/App.css'

function App() {

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/test").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])
  return (
    <div>
      <h1 className="Title"> Race Walking AI </h1>

      <h3> Choose a video to trim</h3>
      {/* {
        (typeof data.test === 'undefined') ? (
          <p> Loading ... </p>
        ) :
          (data.test.map((tes, i) => (
            <p key={i}>{tes}</p>
          ))
        )
      } */}
      <UploadVideo />
    </div>
  )
}

export default App