const sampleSelect = document.querySelector("#sample-select");
const architectureInput = document.querySelector("#architecture-input");
const resultStatus = document.querySelector("#result-status");
const resultSummary = document.querySelector("#result-summary");
const resultChecks = document.querySelector("#result-checks");
let data;

function esc(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[character]);
}

function renderPolicy(policy) {
  document.querySelector("#policy-title").textContent = policy.title;
  document.querySelector("#policy-description").textContent = `${policy.policy_id} · version ${policy.version}`;
  document.querySelector("#legal-context").textContent = policy.legal_context.relationship;
  const link = document.querySelector("#legal-link");
  link.href = policy.legal_context.url;
  document.querySelector("#rule-list").innerHTML = policy.rules.map((rule, index) => {
    const mappings = (rule.ccc_mappings || []).map((mapping) => `<span>${esc(mapping.id)}</span>`).join("");
    const aigf = rule.aigf_reference ? `<span>AIGF draft reference</span>` : "";
    return `<article class="rule"><span class="rule-number">${String(index + 1).padStart(2, "0")}</span><div><strong>${esc(rule.title)}</strong><p>${esc(rule.description)}</p><div class="control-tags">${mappings}${aigf}</div></div></article>`;
  }).join("");
}

function loadSample(name) {
  architectureInput.value = JSON.stringify(data[name], null, 2);
  resultStatus.className = "status-pill idle";
  resultStatus.textContent = "Waiting for a run";
  resultSummary.textContent = "Choose a sample or edit the JSON, then run the policy gate.";
  resultChecks.replaceChildren();
}

function renderResult(result) {
  const passed = result.status === "PASS";
  resultStatus.className = `status-pill ${passed ? "pass" : "fail"}`;
  resultStatus.textContent = passed ? "Policy passed" : "Review required";
  resultSummary.textContent = passed
    ? `${result.checks.length} deterministic checks passed. No legal conclusion is made.`
    : `${result.failure_count} internal policy finding${result.failure_count === 1 ? "" : "s"}. A human review remains necessary.`;
  resultChecks.innerHTML = result.checks.map((check) => {
    const controls = (check.ccc_mappings || []).map((item) => `<span>${esc(item.id)}</span>`).join("");
    const expected = JSON.stringify(check.expected);
    const observed = JSON.stringify(check.observed);
    return `<article class="check-card ${check.status === "PASS" ? "pass" : "fail"}"><div class="check-head"><strong>${esc(check.title)} · ${esc(check.subject)}</strong><span class="check-state">${esc(check.status)}</span></div><p class="check-detail">Expected ${esc(expected)} · observed ${esc(observed)}</p><div class="check-meta">${controls}</div></article>`;
  }).join("");
}

sampleSelect.addEventListener("change", () => loadSample(sampleSelect.value));
document.querySelector("#evaluate-button").addEventListener("click", async () => {
  try {
    const architecture = JSON.parse(architectureInput.value);
    const response = await fetch("/api/evaluate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ architecture })
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "The policy gate could not evaluate this input.");
    renderResult(result);
  } catch (error) {
    resultStatus.className = "status-pill fail";
    resultStatus.textContent = "Input error";
    resultSummary.textContent = error.message;
    resultChecks.replaceChildren();
  }
});

fetch("/api/data")
  .then((response) => response.json())
  .then((loaded) => {
    data = loaded;
    renderPolicy(data.policy);
    loadSample(sampleSelect.value);
  })
  .catch(() => {
    resultStatus.className = "status-pill fail";
    resultStatus.textContent = "Load error";
    resultSummary.textContent = "Could not read the local policy files.";
  });
