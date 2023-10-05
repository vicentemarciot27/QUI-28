import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Hello from './Hello/Hello'
import Parametros from './Parametros/Parametros'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Hello></Hello>
      <Parametros></Parametros>
    </>
  )
}

export default App
