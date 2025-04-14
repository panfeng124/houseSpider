const rows = document.querySelectorAll('tr[bgcolor="#FFFFFF"]');
const tableData = [];

rows.forEach(row => {
    const cells = row.querySelectorAll('td');
    const rowData = Array.from(cells).map(td => td.textContent.trim());
    tableData.push(rowData);
});

console.log(tableData);