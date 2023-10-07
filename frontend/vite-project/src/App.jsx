import React, { useState } from 'react';
import './App.css';
import Hello from './Hello/Hello';
import Parametros from './Parametros/Parametros';
import Modelagem from './Modelagem/Modelagem';

function App() {
  const [points, setPoints] = useState(null); // State to store received points

  // Callback function to receive points and update state
  const receivePoints = (receivedPoints) => {
    setPoints(receivedPoints);
  };

  return (
    <>
      <Hello />
      {/* Pass the callback function as a prop to Parametros */}
      <Parametros onReceivePoints={receivePoints} />
      {/* Pass the points as a prop to Modelagem */}
      <br />
      <br />
      <Modelagem points={points} />
    </>
  );
}

export default App;