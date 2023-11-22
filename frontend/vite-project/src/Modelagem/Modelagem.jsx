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
  const [maximize, setMaximize] = useState(false);
  const [maxPoint, setMaxPoint] = useState([]);
  const [anovaData, setAnovadata] = useState([]);
  const [fTable, setFTable] = useState([]);
  const [fstring, setFstring] = useState();
  const [coefficientstable, setCoefficientsTable] = useState();
  const [residuals_parameters, setResidualsParameters] = useState();
  const [data_plot, setDataPlot] = useState();

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
      points.columns[3],
      points.columns[4],
      points.columns[points.columns.length - 1],
    ];

    // Get the corresponding data for those columns
    const dataOfInterest = points.data.map((row) => [
      row[3],
      row[4],
      row[row.length - 1],
    ]);

    // Convert points data to the desired format
    let formattedData = {
      maximize: maximize,
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
        setMaxPoint(response.data.maxPoint);
        console.log(maxPoint)
        setAnovadata(response.data.anovaTable);
        setFTable(response.data.fTable);
        setFstring(response.data.fstring);
        setCoefficientsTable(response.data.tabela_coeficientes);
        setResidualsParameters(response.data.residuals_parameters);
        setDataPlot(response.data.data_plot);
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
                {points.columns.slice(1).map((column, idx) => (
                  <th key={idx}>{column}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {points.data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {row.slice(1).map((cell, cellIndex) => (
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
      <p>Maximizar? (Padrão é minimizar)</p>
      <input
        type="checkbox"
        checked={maximize}
        onChange={(event) => setMaximize(event.target.checked)}
      />
      <br />
      <button className="SendBtn" onClick={handleSendClick}>
        Processar dados
      </button>.
      {
        data_plot && 
        <img
        src={`data:image/png;base64,${data_plot}`}
        style={{ width: 550, padding: "1rem" }}
        alt="Quadratic Plot"
      />
      }
      
      {imageBase64 && (
        <img
          src={`data:image/png;base64,${imageBase64}`}
          style={{ width: 550, padding: "1rem" }}
          alt="Quadratic Plot"
        />
      )}
      <h3>
        O ponto de inflexão desejado é:{" "}
        {maxPoint.map((point) => {
          return <h3>{point}</h3>;
        })}
      </h3>
      {anovaData && (
        <div>
          <h2>ANOVA Table</h2>
          <table>
            <thead>
              <tr>
                <th>Fonte de Variação</th>
                <th>Soma Quadrática</th>
                <th>Número de Graus de Liberdade</th>
                <th>Média Quadrática</th>
              </tr>
            </thead>
            <tbody>
              {anovaData.map((row, index) => (
                <tr key={index}>
                  <td>{row["Fonte de Variação"]}</td>
                  <td>{row["Soma Quadrática"]}</td>
                  <td>{row["Número de Graus de Liberdade"]}</td>
                  <td>{row["Média Quadrática"]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {fTable && (
        <div>
          <h2>F Table</h2>
          <br />
          <table>
            <thead>
              <tr>
                <th>Parâmetro Estatístico</th>
                <th>Valor</th>
              </tr>
            </thead>
            <tbody>
              {fTable.map((row, index) => (
                <tr key={index}>
                  <td>{row["Parâmetro Estatístico"]}</td>
                  <td>{row["Valor"]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {fstring}
      {coefficientstable && (
        <div>
          <h2>Coefficients Table</h2>
          <br />
          <table  style={{margin: "auto"}}>
            <thead>
              <tr>
                <th>Parâmetro Estatístico</th>
                <th>Valor</th>
                <th>Erros-Padrão</th>
              </tr>
            </thead>
            <tbody>
              {coefficientstable.map((row, index) => (
                <tr key={index}>
                  <td>{row["Coeficiente"]}</td>
                  <td>{row["Valor"]}</td>
                  <td>{row["Erros-Padrão"]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {
        residuals_parameters && 
        <img
        src={`data:image/png;base64,${residuals_parameters}`}
        style={{ width: 550, padding: "1rem" }}
        alt="Quadratic Plot"
      />
      }
      
    </div>
  );
};

export default Modelagem;
