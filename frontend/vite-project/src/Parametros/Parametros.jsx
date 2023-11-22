import React, { useState } from "react";
import "./Parametros.css";
import { renderTable } from "./DataTable";

import axios from "axios";

function VariableForm(props) {
  const [state, setState] = useState({
    numVariables: 0,
    alpha: 1,
    variables: [],
    has_integer: false,
  });

  const [response, setResponse] = useState(null);
  const [errorMessages, setErrorMessages] = useState([]);
  const [tableData, setTableData] = useState(null);


  // HANDLE CHANGES FUNCTIONS
  // Handle global inputs (like alpha)
  function handleGlobalInputChange(field, value) {
    setState({
      ...state,
      [field]: Number(value),
    });
  }

  function getRandomValue(min, max) {
    return Math.random() * (max - min) + min;
  }

  // Generates new variables from changing the number of variables
  function handleNumVariablesChange(e) {
    const numVariables = parseInt(e.target.value, 10);
    const currentVariables = state.variables;
    let newVariables;

    if (numVariables > currentVariables.length) {
      // If the new count is greater, append new variables
      newVariables = [
        ...currentVariables,
        ...Array.from(
          { length: numVariables - currentVariables.length },
          () => ({
            name: `Variable${Math.floor(getRandomValue(1, 100))}`, // Random name from "Variable1" to "Variable99"
            unit: `Unit${Math.floor(getRandomValue(1, 10))}`, // Random unit from "Unit1" to "Unit9"
            value: `${getRandomValue(1, 10).toFixed(2)}`, // Random value between 1 and 10 with 2 decimal places
            maxValue: "10",
            minValue: "0",
            delta: `${getRandomValue(0.1, 1).toFixed(2)}`, // Random delta between 0.1 and 1 with 2 decimal places
            alpha: state.alpha,
            results: 0,
          })
        ),
      ];
    } else {
      // If the new count is less, slice the array to the new count
      newVariables = currentVariables.slice(0, numVariables);
    }

    setState({
      ...state,
      numVariables,
      variables: newVariables,
    });
  }

  // Handle Variable input
  function handleVariableChange(index, field, value) {
    const newVariables = [...state.variables];
    newVariables[index][field] = value;
    setState({
      ...state,
      variables: newVariables,
    });
  }

  // CORE FUNCTIONS
  // Handle form submission
  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:5000/submit_param",
        state
      );
      setResponse(response.data);
      setTableData(response.data);
      setErrorMessages([]); // Clear any previous errors on successful call

      // Pass the points to the parent component
      props.onReceivePoints(response.data);
    } catch (error) {
      if (error.response && error.response.data && error.response.data.errors) {
        // Backend returned an array of error messages
        setErrorMessages(error.response.data.errors || "An error occured");3
        console.log("Hello it's me")
      } else {
        // Some other error like network failure
        setErrorMessages(["An error occurred while processing your request."]);
      }
      console.error(error);
    }
  }
  // Export as JSON
  function exportAsJSON() {
    const blob = new Blob([JSON.stringify(response.data)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "data.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  // Export as TXT
  function exportAsTXT() {
    const blob = new Blob([JSON.stringify(response.data, null, 2)], {
      type: "text/plain",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "data.txt";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <>
    <h2>Parametragem:</h2>
    <form id="Parametros" onSubmit={handleSubmit}>
      <label>
        Number of Variables: <br />
        <input
          type="number"
          value={state.numVariables}
          onChange={handleNumVariablesChange}
        />
      </label>
      {/* Input for global alpha */}
      <label>
        Alpha: <br />
        <input
          type="number"
          value={state.alpha || 0}
          onChange={(e) => handleGlobalInputChange("alpha", e.target.value)}
          placeholder="Enter global alpha value"
        />
      </label>
      {/* <label>
        Integer:
        <input
          type="checkbox"
          checked={state.has_integer}
          onChange={(e) =>
            handleGlobalInputChange("has_integer", e.target.checked)
          }
        />
      </label> */}
      {state.variables.map((variable, index) => (
        <div className="InputsdeVar" key={index}>
          <h2>Variable {index + 1}:</h2>
          <div>
            <label>
              Name: <br />
              <input
                type="text"
                value={variable.name || ""}
                onChange={(e) =>
                  handleVariableChange(index, "name", e.target.value)
                }
                placeholder="Enter name" // <-- added placeholder
              />
            </label>
            <label>
              Unit: <br />
              <input
                type="text"
                value={variable.unit || ""}
                onChange={(e) =>
                  handleVariableChange(index, "unit", e.target.value)
                }
                placeholder="Enter unit" // <-- added placeholder
              />
            </label>
            <label>
              Value: <br />
              <input
                type="number"
                value={variable.value || ""}
                onChange={(e) =>
                  handleVariableChange(index, "value", e.target.value)
                }
                placeholder="Enter value"
              />
            </label>

            <label>
              Max: <br />
              <input
                type="number"
                value={variable.maxValue || ""}
                onChange={(e) =>
                  handleVariableChange(index, "maxValue", e.target.value)
                }
                placeholder="10" // <-- added placeholder
              />
            </label>
            <label>
              Min: <br />
              <input
                type="number"
                value={variable.minValue || ""}
                onChange={(e) =>
                  handleVariableChange(index, "minValue", e.target.value)
                }
                placeholder="0" // <-- added placeholder
              />
            </label>
            <label>
              Delta: <br />
              <input
                type="number"
                value={variable.delta || ""}
                onChange={(e) =>
                  handleVariableChange(index, "delta", e.target.value)
                }
                placeholder="0.1" // <-- added placeholder
              />
            </label>
          </div>
        </div>
      ))}
      <div className="buttons">
        <button type="button" className="SendBtn" onClick={exportAsJSON}>
          Export as JSON
        </button>
        <button type="submit" className="SendBtn">
          Process Data
        </button>
        <button type="button" className="SendBtn" onClick={exportAsTXT}>
          Export as TXT
        </button>
      </div>

      {errorMessages.length == 0 && response && (
        <div className="response-data">
          <h2>Received Data:</h2>
          <p>{renderTable(tableData)}</p>
        </div>
      )}
      {errorMessages.length > 0 && (
        <div className="error-messages">
          {errorMessages.map((errorMessage, index) => (
            <div key={index} className="error-message">
              {errorMessage}
            </div>
          ))}
        </div>
      )}
    </form>
    </>
  );
}

export default VariableForm;
