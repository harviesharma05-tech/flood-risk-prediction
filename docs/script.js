// Runs the exported RandomForest (model.js -> scoreFlood) entirely in the
// browser. No server, no network request — GitHub Pages friendly.

const FIELD_ORDER = [
  "rainfall_mm", "water_level_m", "river_discharge_cms", "temperature_c",
  "humidity_pct", "soil_moisture_pct", "elevation_m", "drainage_quality",
  "historical_floods_5yr", "population_density",
];

// scoreFlood() class order matches scikit-learn's alphabetical LabelEncoder
const CLASS_ORDER = ["High", "Low", "Medium"];
const RISK_COLOR = { Low: "#22c55e", Medium: "#f59e0b", High: "#ef4444" };

const form = document.getElementById("predict-form");
const errorBox = document.getElementById("error-box");
const resultCard = document.getElementById("result-card");
const resultActions = document.getElementById("result-actions");
const introSection = document.getElementById("intro-section");
const resetBtn = document.getElementById("reset-btn");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  errorBox.style.display = "none";

  const values = [];
  for (const key of FIELD_ORDER) {
    const raw = document.getElementById(key).value;
    const num = parseFloat(raw);
    if (Number.isNaN(num)) {
      errorBox.textContent = "Please fill in every field with a valid number.";
      errorBox.style.display = "block";
      return;
    }
    values.push(num);
  }

  const scores = scoreFlood(values); // [pHigh, pLow, pMedium]
  const total = scores.reduce((a, b) => a + b, 0) || 1;
  const probs = scores.map((s) => (s / total) * 100);

  let maxIdx = 0;
  for (let i = 1; i < probs.length; i++) {
    if (probs[i] > probs[maxIdx]) maxIdx = i;
  }
  const label = CLASS_ORDER[maxIdx];
  const confidence = probs[maxIdx].toFixed(1);

  renderResult(label, confidence, probs);
});

function renderResult(label, confidence, probs) {
  document.getElementById("risk-value").textContent = label;
  document.getElementById("risk-value").style.color = RISK_COLOR[label];
  resultCard.style.setProperty("--risk-color", RISK_COLOR[label]);
  document.getElementById("confidence-text").textContent = `${confidence}% model confidence`;

  const barsWrap = document.getElementById("prob-bars");
  barsWrap.innerHTML = "";
  CLASS_ORDER.forEach((cls, i) => {
    const pct = probs[i].toFixed(1);
    const row = document.createElement("div");
    row.className = "prob-row";
    row.innerHTML = `
      <span class="prob-name">${cls}</span>
      <div class="prob-track"><div class="prob-fill" style="width:${pct}%;"></div></div>
      <span class="prob-pct">${pct}%</span>
    `;
    barsWrap.appendChild(row);
  });

  introSection.style.display = "none";
  form.style.display = "none";
  resultCard.style.display = "block";
  resultActions.style.display = "flex";
  window.scrollTo({ top: 0, behavior: "smooth" });
}

resetBtn.addEventListener("click", () => {
  form.reset();
  form.style.display = "grid";
  introSection.style.display = "block";
  resultCard.style.display = "none";
  resultActions.style.display = "none";
  errorBox.style.display = "none";
});
