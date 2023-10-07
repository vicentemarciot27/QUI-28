  // RENDERING FUNCTIONS
  const shuffle = (array) => {
    const arr2 = array;
    for (let i = arr2.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr2[i], arr2[j]] = [arr2[j], arr2[i]];
    }
    return arr2;
  };

  function renderTable(tableData) {
    if (!tableData) return null;

    return (
      <div>
        <table>
          <thead>
            <tr>
              {tableData.columns.map((column, idx) => (
                <th key={idx}>{column}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tableData.data.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {row.map((cell, cellIndex) => (
                  <td key={cellIndex}>{cell}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        <h2>Ordem Recomendada:</h2>
        <table>
          <thead>
            <tr>
              {tableData.columns.map((column, idx) => (
                <th key={idx}>{column}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {shuffle(
              tableData.data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {row.map((cell, cellIndex) => (
                    <td key={cellIndex}>{cell}</td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    );
  }

export {renderTable};