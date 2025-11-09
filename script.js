let currentWeekOffset = 0;
let newsData = [];

function loadJSON() {
  fetch("data/usd-high-impact.json")
    .then(res => {
      if (!res.ok) throw new Error("Failed to load JSON");
      return res.json();
    })
    .then(data => {
      newsData = data;
      renderWeek();
    })
    .catch(err => {
      console.error("Error loading JSON:", err);
      document.getElementById("newsTable").innerHTML =
        `<tr><td colspan="5">⚠️ Could not load data.</td></tr>`;
    });
}

function renderWeek() {
  const today = new Date();
  const start = getStartOfWeek(addWeeks(today, currentWeekOffset));
  const end = new Date(start);
  end.setDate(start.getDate() + 6);

  document.getElementById("weekRange").textContent =
    `${formatDate(start)} – ${formatDate(end)}`;

  const tbody = document.getElementById("newsTable");
  tbody.innerHTML = "";

  const weekEvents = newsData.filter(event => {
    const eventDate = new Date(event.date);
    return eventDate >= start && eventDate <= end;
  });

  if (weekEvents.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5">📭 No high-impact USD news this week</td></tr>`;
    return;
  }

  weekEvents.forEach(event => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td data-label="Date">${event.date}</td>
      <td data-label="Time">${event.time}</td>
      <td data-label="Event">${event.event}</td>
      <td data-label="Impact">🔴 ${event.impact}</td>
      <td data-label="Forecast">${event.forecast}</td>
    `;
    tbody.appendChild(row);
  });
}

document.getElementById("prevWeek").addEventListener("click", () => {
  currentWeekOffset -= 1;
  renderWeek();
});

document.getElementById("nextWeek").addEventListener("click", () => {
  currentWeekOffset += 1;
  renderWeek();
});

// Utilities
function addWeeks(date, weeks) {
  const newDate = new Date(date);
  newDate.setDate(date.getDate() + weeks * 7);
  return newDate;
}

function getStartOfWeek(date) {
  const d = new Date(date);
  const day = d.getDay(); // Sunday = 0
  const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Monday
  return new Date(d.setDate(diff));
}

function formatDate(dateObj) {
  return dateObj.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric"
  });
}

loadJSON();
