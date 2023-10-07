import React, { useState } from "react";
import "./Modelagem.css";

const Modelagem = (props) => {
  const [willRender, setWillRender] = useState(false);
  const [points, setPoints] = useState({
    columns: [], // Initialize without "results"
    data: [],
  });

  const handleButtonClick = () => {
    // Update the points state when the button is clicked
    setPoints({
      columns: [...props.points.columns, "Result"], // Include "Result" as a column
      data: props.points.data,
    });
    setWillRender(true);
  };

  const shuffle = (array) => {
    const arr2 = array;
    for (let i = arr2.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr2[i], arr2[j]] = [arr2[j], arr2[i]];
    }
    return arr2;
  };

  return (
    <div id="Modelagem" className="">
      <h2>Modelagem</h2>
      <p>Recebe dados da parametragem e os coloca em um modelo quadrático</p>
      <button className="SendBtn" onClick={handleButtonClick}>
        Receber Dados
      </button>
      <br />
      <br />
      {willRender && (
        <div>
          <table>
            <thead>
              <tr>
                {points.columns.map((column, idx) => (
                  <th key={idx}>{column}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {
                points.data.map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {row.map((cell, cellIndex) => (
                      <td key={cellIndex}>{cell}</td>
                    ))}
                    <td>
                      <input
                        type="text"
                        value={points.data[rowIndex].Result || ""}
                        onChange={(e) => {
                          // Update the "Result" value in the data
                          const newData = [...points.data];
                          newData[rowIndex].Result = e.target.value;
                          setPoints({
                            ...points,
                            data: newData,
                          });
                        }}
                      />
                    </td>
                  </tr>
                ))
              }
            </tbody>
          </table>
        </div>
      )}
      <button className="SendBtn" onClick={handleButtonClick}>
        Processar dados
      </button>
    </div>
  );
};

export default Modelagem;
