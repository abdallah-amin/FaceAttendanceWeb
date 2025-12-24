const statusText = document.getElementById("statusText");

const todayEl = document.getElementById("today");
const presentCountEl = document.getElementById("presentCount");
const presentPill = document.getElementById("presentPill");
const presentList = document.getElementById("presentList");

// أزرار الإضافة
const btnAddFromImage = document.getElementById("btnAddFromImage");
const btnAddFromCamera = document.getElementById("btnAddFromCamera");

function setStatus(msg) {
  if (statusText) statusText.textContent = msg;
}

function clearNode(node) {
  if (!node) return;
  while (node.firstChild) node.removeChild(node.firstChild);
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
   Render Present Table
======================= */
function renderPresent(items) {
  clearNode(presentList);

  if (!items || items.length === 0) {
    const div = document.createElement("div");
    div.className = "row item";
    div.innerHTML = `<div>No attendance recorded yet</div><div class="badge">—</div>`;
    presentList.appendChild(div);
    return;
  }

  items.forEach(it => {
    const div = document.createElement("div");
    div.className = "row item";
    div.innerHTML = `
      <div>${escapeHtml(it.name)}</div>
      <div class="badge good">${escapeHtml(it.time || "—")}</div>
    `;
    presentList.appendChild(div);
  });
}

/* =======================
   Fetch Status
======================= */
async function refreshStatus() {
  try {
    setStatus("Updating...");
    const res = await fetch("/api/status", { cache: "no-store" });
    const j = await res.json();

    if (!j.ok) throw new Error(j.error || "Unknown error");

    const d = j.data;

    if (todayEl) todayEl.textContent = d.date;
    if (presentCountEl) presentCountEl.textContent = d.present_count;
    if (presentPill) presentPill.textContent = `${d.present_count} present`;

    renderPresent(d.present);

    setStatus("Ready");
  } catch (e) {
    console.error(e);
    setStatus("Error");
  }
}

/* =======================
   Add Person - Upload Image
======================= */
if (btnAddFromImage) {
  btnAddFromImage.addEventListener("click", async () => {
    const name = prompt("Enter person name:");
    if (!name) return;

    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";

    input.onchange = async () => {
      const file = input.files[0];
      if (!file) return;

      const form = new FormData();
      form.append("name", name);
      form.append("image", file);

      try {
        setStatus("Uploading...");
        const res = await fetch("/api/add_person/upload", {
          method: "POST",
          body: form
        });

        const j = await res.json();
        if (!j.ok) throw new Error(j.error);

        alert("Person added successfully");
        setStatus("Ready");
      } catch (e) {
        alert(e.message);
        setStatus("Error");
      }
    };

    input.click();
  });
}

/* =======================
   Add Person - From Camera (Unknown)
======================= */
if (btnAddFromCamera) {
  btnAddFromCamera.addEventListener("click", async () => {
    const name = prompt("Enter person name:");
    if (!name) return;

    try {
      setStatus("Adding from camera...");
      const res = await fetch("/api/add_person/from_camera", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
      });

      const j = await res.json();
      if (!j.ok) throw new Error(j.error);

      alert("Person added from camera");
      setStatus("Ready");
    } catch (e) {
      alert(e.message);
      setStatus("Error");
    }
  });
}

/* =======================
   Initial Load
======================= */
refreshStatus();
setInterval(refreshStatus, 5000);
