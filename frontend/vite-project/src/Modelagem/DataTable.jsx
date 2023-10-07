// RENDERING FUNCTIONS
const shuffle = (array) => {
  const arr2 = array;
  for (let i = arr2.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr2[i], arr2[j]] = [arr2[j], arr2[i]];
  }
  return arr2;
};

function renderTable(tableData, onResultChange) {
  if (!tableData) return null;

  return (
    <div>
      <h2>Ordem Recomendada:</h2>
      <table>
        <thead>
          <tr>
            {tableData.columns.map((column, idx) => (
              <th key={idx}>{column}</th>
            ))}
            <th>Result</th> {/* Add a Result column header */}
          </tr>
        </thead>
        <tbody>
          {shuffle(
            tableData.data.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {row.map((cell, cellIndex) => (
                  <td key={cellIndex}>{cell}</td>
                ))}
                <td>
                  <input
                    type="text"
                    value={tableData.results[rowIndex] || ""}
                    onChange={(e) => onResultChange(rowIndex, e.target.value)}
                  />
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export { renderTable };
