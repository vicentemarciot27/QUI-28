import React, { useState } from "react";
import "./Parametros.css";

function VariableForm() {
  const [state, setState] = useState({
    numVariables: 0,
    variables: [],
  });

  // Generates new variables from changing the number of variables
  function handleNumVariablesChange(e) {
    const numVariables = e.target.value;
    setState({
      numVariables,
      variables: Array.from({ length: numVariables }, () => ({
        name: "",
        unit: "",
        maxValue: "",
        minValue: "",
        delta: "",
        alpha: "",
      })),
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

  // Handle form submission
  async function handleSubmit(e) {
    e.preventDefault();
    try {
      // Send a POST request to the Flask backend
      const response = await axios.post("http://localhost:5000/submit", state);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  }

  // Export as JSON
  function exportAsJSON() {
    const blob = new Blob([JSON.stringify(state)], {
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
    const blob = new Blob([JSON.stringify(state, null, 2)], {
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
    <form id="Parametros" onSubmit={handleSubmit}>
      <label>
        Number of Variables:
        <input
          type="number"
          value={state.numVariables}
          onChange={handleNumVariablesChange}
        />
      </label>
      {state.variables.map((variable, index) => (
        <div className="InputsdeVar">
          <h2>Variable {index}:</h2>
          <div key={index}>
            <label>
              Name: <br />
              <input
                type="text"
                value={variable.name}
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
                value={variable.unit}
                onChange={(e) =>
                  handleVariableChange(index, "unit", e.target.value)
                }
                placeholder="Enter unit" // <-- added placeholder
              />
            </label>
            <label>
              Max: <br />
              <input
                type="number"
                value={variable.maxValue}
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
                value={variable.minValue}
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
                value={variable.delta}
                onChange={(e) =>
                  handleVariableChange(index, "delta", e.target.value)
                }
                placeholder="0.1" // <-- added placeholder
              />
            </label>
            <label>
              Alpha: <br />
              <input
                type="number"
                value={variable.alpha}
                onChange={(e) =>
                  handleVariableChange(index, "alpha", e.target.value)
                }
                placeholder="0.5" // <-- added placeholder
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
    </form>
  );
}

export default VariableForm;
