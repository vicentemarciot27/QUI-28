import React, { useState } from "react";
import axios from "axios";
import "./Modelagem.css";

const Modelagem = (props) => {
  const [willRender, setWillRender] = useState(false);
  const [points, setPoints] = useState({
    columns: [], // Initialize without "results"
    data: [],
  });
  const [imageBase64, setImageBase64] = useState("");

  const handleButtonClick = () => {
    // Update the points state when the button is clicked
    setPoints({
      columns: [...props.points.columns, "Resposta"], // Include "Result" as a column
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

  const handleSendClick = () => {
    // Exclude the first column from the data when sending the request
    // Get the two columns after the first and exclude the last one
    // Get columns 2, 3, and the last one
    const columnsOfInterest = [
      points.columns[1],
      points.columns[2],
      points.columns[points.columns.length - 1],
    ];

    // Get the corresponding data for those columns
    const dataOfInterest = points.data.map((row) => [
      row[1],
      row[2],
      row[row.length - 1],
    ]);

    // Convert points data to the desired format
    let formattedData = {
      data_frame: {
        columns: columnsOfInterest,
        data: dataOfInterest,
      },
    };

    // Send a POST request to the backend using axios
    axios
      .post("http://localhost:5000/submit_quadratic_model", formattedData)
      .then((response) => {
        setImageBase64(response.data.plot);
      })
      .catch((error) => {
        console.error("There was an error processing the data:", error);
      });
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
              {points.data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {row.map((cell, cellIndex) => (
                    <td key={cellIndex}>{cell}</td>
                  ))}
                  <td>
                    <input
                      type="number"
                      value={
                        points.data[rowIndex][points.columns.length - 1] || ""
                      }
                      onChange={(e) => {
                        // Update the last element in the row (Resposta) value in the data
                        const newData = [...points.data];
                        newData[rowIndex][points.columns.length - 1] =
                          e.target.value;
                        setPoints({
                          ...points,
                          data: newData,
                        });
                        console.log(points.data);
                      }}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <button className="SendBtn" onClick={handleSendClick}>
        Processar dados
      </button>
      {imageBase64 && (
        <img
          src={`data:image/png;base64,${imageBase64}`}
          alt="Quadratic Plot"
        />
      )}
    </div>
  );
};

export default Modelagem;
