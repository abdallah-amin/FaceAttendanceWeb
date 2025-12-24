const dateInput = document.getElementById("dateInput");
const tableBody = document.getElementById("tableBody");

const btnSearch = document.getElementById("btnSearch");
const btnDownload = document.getElementById("btnDownload");
const btnToday = document.getElementById("btnToday");

/* =======================
   Helpers
======================= */
function clearTable() {
  while (tableBody.firstChild) {
    tableBody.removeChild(tableBody.firstChild);
  }
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

/* =======================
   Render
======================= */
function renderRows(items) {
  clearTable();

  if (!items || items.length === 0) {
    const div = document.createElement("div");
    div.className = "row item";
    div.innerHTML = `<div>No attendance for this date</div><div class="badge">—</div>`;
    tableBody.appendChild(div);
    return;
  }

  items.forEach(p => {
    const div = document.createElement("div");
    div.className = "row item";
    div.innerHTML = `
      <div>${escapeHtml(p.name)}</div>
      <div class="badge good">${escapeHtml(p.time)}</div>
    `;
    tableBody.appendChild(div);
  });
}

/* =======================
   Load Attendance
======================= */
async function loadAttendance(date = null) {
  try {
    const url = date
      ? `/api/status?date=${date}`
      : "/api/status";

    const res = await fetch(url, { cache: "no-store" });
    const json = await res.json();

    if (!json.ok) {
      throw new Error(json.error || "Failed to load attendance");
    }

    renderRows(json.data.present);
  } catch (err) {
    console.error(err);
    clearTable();
  }
}

/* =======================
   Download CSV
======================= */
function downloadCSV() {
  const date = dateInput.value;
  const url = date
    ? `/api/attendance/csv?date=${date}`
    : "/api/attendance/csv";

  window.location.href = url;
}

/* =======================
   Events
======================= */
btnSearch.addEventListener("click", () => {
  loadAttendance(dateInput.value);
});

btnToday.addEventListener("click", () => {
  dateInput.value = "";   // فضي التاريخ
  loadAttendance();       // حمّل حضور النهارده
});

btnDownload.addEventListener("click", downloadCSV);

/* =======================
   Initial Load (Today)
======================= */
loadAttendance();
