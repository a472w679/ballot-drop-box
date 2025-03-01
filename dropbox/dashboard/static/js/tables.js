function showTable(boxId) {
  const tables = document.querySelectorAll(".table-container");
  tables.forEach((table) => table.classList.add("hidden"));
  document.getElementById(boxId).classList.remove("hidden");
}
