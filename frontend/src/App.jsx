import React, { useState } from 'react'

const GATEWAY = import.meta.env.VITE_GATEWAY_URL || 'http://localhost:8000'

export default function App() {
  const [predict, setPredict] = useState(null)
  const [orders, setOrders] = useState([])

  const doPredict = async () => {
    const r = await fetch(`${GATEWAY}/predict`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({features:[5.1,3.5,1.4,0.2]})
    });
    setPredict(await r.json())
  }

  const getOrders = async () => {
    const r = await fetch(`${GATEWAY}/orders`)
    setOrders(await r.json())
  }

  return (
    <div style={{fontFamily:'sans-serif', padding:16}}>
      <h1>Cloud‑Native MLOps Demo</h1>
      <button onClick={doPredict}>Predict (Iris sample)</button>
      {predict && <pre>{JSON.stringify(predict, null, 2)}</pre>}

      <button onClick={getOrders} style={{marginLeft:8}}>Fetch Orders</button>
      <pre>{JSON.stringify(orders, null, 2)}</pre>

      <p style={{opacity:0.7}}>Gateway: {GATEWAY}</p>
    </div>
  )
}
