/* A transparent replay of Python outputs. No API, hidden AI, or simulated typing. */
"use strict";
const { workflow, evaluation: report, integrity } = window.CSM_DATA;
let selected = 0,
  integration = 0,
  activeTab = "evidence",
  language = "en",
  updated = false;
const $ = (id) => document.getElementById(id);
const esc = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const badge = (status) =>
  `<span class="badge ${esc(status)}">${esc(status.replaceAll("_", " "))}</span>`;
function renderQueue() {
  $("accounts").innerHTML = workflow.packets
    .map(
      (p, n) =>
        `<button class="account ${n === selected ? "active" : ""}" data-account="${n}" aria-pressed="${n === selected}"><b>${esc(p.selection.name)}</b><span>${esc(p.context.integrations[0].app)}</span><span class="queue-meta"><small class="urgent">Launch in ${p.selection.days_to_launch}d</small><small>Contact ${p.selection.days_since_contact}d ago</small></span></button>`,
    )
    .join("");
  document.querySelectorAll("[data-account]").forEach((button) =>
    button.addEventListener("click", () => {
      selected = Number(button.dataset.account);
      integration = 0;
      renderQueue();
      renderCase();
    }),
  );
}
function checksTable(r) {
  return `<div class="decision">${badge(r.decision)}<strong>${esc(r.platform)} · scoped checklist</strong></div><table class="checks"><thead><tr><th>CHECK / SOURCE</th><th>STATE</th><th>EVIDENCE</th></tr></thead><tbody>${r.checks.map((c) => `<tr><td>${esc(c.label)}<a class="check-source" href="${esc(c.source_url)}" target="_blank" rel="noreferrer">${c.authority === "project_policy" ? "Project policy · related docs" : "Official documentation"} ↗</a></td><td>${badge(c.status)}</td><td>${c.evidence_ids.length ? c.evidence_ids.map((id) => `<span class="evidence-link">${esc(id)}</span>`).join("") : '<span class="evidence-link">No applicable record</span>'}</td></tr>`).join("")}</tbody></table><p class="boundary">${esc(r.boundary)}</p>`;
}
function renderCase() {
  const p = workflow.packets[selected],
    item = p.integrations[integration],
    r = item.readiness;
  $("account-heading").innerHTML =
    `<div><h3>${esc(p.selection.name)}</h3><p>${esc(r.app)} · ${esc(p.selection.stage)} · ${esc(p.selection.account_id)}</p></div><label><span class="small-label">PLATFORM </span><select id="platform-select" aria-label="Integration platform">${p.integrations.map((it, n) => `<option value="${n}" ${n === integration ? "selected" : ""}>${esc(it.readiness.platform)}</option>`).join("")}</select></label>`;
  $("platform-select").addEventListener("change", (e) => {
    integration = Number(e.target.value);
    renderCase();
  });
  document.querySelectorAll("[data-tab]").forEach((b) => {
    b.setAttribute("aria-selected", String(b.dataset.tab === activeTab));
    b.tabIndex = b.dataset.tab === activeTab ? 0 : -1;
  });
  $("panel").setAttribute("aria-labelledby", `tab-${activeTab}`);
  if (activeTab === "evidence") {
    const issue = p.context.issues.find(
      (i) => i.integration_id === r.integration_id,
    );
    const e = issue
      ? p.context.evidence.find((e) => e.id === issue.evidence_id)
      : null;
    $("panel").innerHTML =
      (e
        ? `<div class="quote"><p>${esc(issue.summary)}</p><details><summary>Read original customer message</summary><p lang="${e.language === "zh" ? "zh-CN" : "en"}">${esc(e.text)}</p></details><small>CUSTOMER REPORT · ${esc(e.id)} · ${esc(e.at.slice(0, 10))}</small></div>`
        : '<div class="quote"><p>No issue message recorded for this integration. Readiness still depends on its own evidence.</p></div>') +
      checksTable(r) +
      `<details><summary>Inspect the supporting evidence records</summary><pre>${esc(
        JSON.stringify(
          p.context.evidence.filter((e) =>
            r.checks.some((c) => c.evidence_ids.includes(e.id)),
          ),
          null,
          2,
        ),
      )}</pre></details>`;
  } else if (activeTab === "followup") {
    const draft = item[`followup_${language}`];
    $("panel").innerHTML =
      `<div class="toolbar"><label for="language-select">Client language</label><select id="language-select"><option value="en" ${language === "en" ? "selected" : ""}>English</option><option value="zh" ${language === "zh" ? "selected" : ""}>中文</option></select><button class="copy" id="copy-draft">Copy draft</button></div><div class="draft-purpose"><strong>Purpose: ${esc(draft.intent.replaceAll("_", " "))}</strong><p>${esc(draft.next_action)}</p></div><pre class="draft" lang="${language === "zh" ? "zh-CN" : "en"}">${esc(draft.body)}</pre><div class="notice"><b>DRAFT · NOT SENT</b> — Contact history is unchanged. Deterministic template; a host model may rewrite it with evidence-bound review.</div><details><summary>Inspect draft provenance and review limits</summary><pre>${esc(JSON.stringify({ evidence_ids: draft.evidence_ids, issue_ids: draft.issue_ids, review: draft.review, requests: draft.requests }, null, 2))}</pre></details>`;
    $("language-select").addEventListener("change", (e) => {
      language = e.target.value;
      renderCase();
    });
    $("copy-draft").addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(draft.body);
        $("copy-draft").textContent = "Copied";
      } catch {
        $("copy-draft").textContent = "Select text to copy";
      }
    });
  } else {
    const issue = p.context.issues.find(
      (i) => i.integration_id === r.integration_id,
    );
    const t = issue
      ? p.tickets.find((t) => t.draft_id === `ticket-${issue.id}`)
      : null;
    if (!t) {
      $("panel").innerHTML =
        '<div class="empty"><h3>No issue to escalate yet.</h3><p>Request missing evidence in the follow-up. A readiness unknown does not automatically become a support ticket.</p></div>';
      return;
    }
    $("panel").innerHTML =
      `<h3>${esc(t.title)}</h3><div class="decision">${badge(t.handoff_state)}<strong>Root cause: ${esc(t.root_cause)}</strong></div><dl class="ticket-fields">${Object.entries(
        t.fields,
      )
        .map(
          ([k, v]) =>
            `<dt>${esc(k.replaceAll("_", " "))}</dt><dd>${esc(v)}</dd>`,
        )
        .join(
          "",
        )}<dt>Evidence</dt><dd>${esc(t.evidence_ids.join(", "))}</dd><dt>Suggested owner</dt><dd>${esc(t.suggested_owner)}</dd></dl><div class="missing"><strong>${t.missing_fields.length ? "Request before technical review" : "Ready for handoff review"}</strong>${t.missing_fields.length ? t.missing_fields.map((f) => `<code>${esc(f)}</code>`).join(" ") : "All scoped required fields are present. Confirm their content and the appropriate owner before submission."}</div><p class="boundary">${esc(t.next_action)}</p>${t.triage.notes.map((n) => `<p class="boundary">${esc(n)}</p>`).join("")}<details><summary>Inspect candidate checks and source URLs</summary><pre>${esc(JSON.stringify(t.triage, null, 2))}</pre></details><details><summary>Trace each handoff field to its record</summary><pre>${esc(JSON.stringify(t.field_sources, null, 2))}</pre></details>`;
  }
}
document.querySelectorAll("[data-tab]").forEach((b, n, buttons) => {
  b.addEventListener("click", () => {
    activeTab = b.dataset.tab;
    renderCase();
  });
  b.addEventListener("keydown", (event) => {
    let next;
    if (event.key === "ArrowRight") next = (n + 1) % buttons.length;
    if (event.key === "ArrowLeft")
      next = (n + buttons.length - 1) % buttons.length;
    if (event.key === "Home") next = 0;
    if (event.key === "End") next = buttons.length - 1;
    if (next !== undefined) {
      event.preventDefault();
      buttons[next].click();
      buttons[next].focus();
    }
  });
});
function renderCounter() {
  const r = workflow.counterfactual[updated ? "after" : "before"];
  $("counterfactual").innerHTML =
    `<span class="small-label">${updated ? "AFTER CUSTOMER UPDATE" : "ORIGINAL EVIDENCE"}</span><div class="decision">${badge(r.decision)}<strong>Moon Garden / Android</strong></div>${r.checks
      .filter((c) =>
        ["currency_approved", "test_only_off", "device_verified"].includes(
          c.id,
        ),
      )
      .map(
        (c) =>
          `<div class="counter-row"><span>${esc(c.label)}</span>${badge(c.status)}</div>`,
      )
      .join(
        "",
      )}<p style="margin-top:17px">${updated ? "The settings are now customer-confirmed. The failed device check and missing callback verification remain unresolved." : "Two settings are unknown. A non-test device failure is already recorded."}</p>`;
  $("update-toggle").setAttribute("aria-pressed", String(updated));
  $("update-toggle").textContent = updated
    ? "Reset to original evidence ↺"
    : "Apply the synthetic customer update →";
}
$("update-toggle").addEventListener("click", () => {
  updated = !updated;
  renderCounter();
});
const m = report.metrics.holdout;
$("score").innerHTML = `${m.correct}<small> / ${m.total} messages</small>`;
const seen = new Set();
$("failures").innerHTML = report.triage_cases
  .filter(
    (c) =>
      !c.correct &&
      c.lang === "en" &&
      !seen.has(c.family) &&
      seen.add(c.family),
  )
  .map(
    (c) =>
      `<div class="failure"><span>“${esc(c.text)}”</span><strong>Expected: ${esc(c.expected.join(" + "))} → retrieved: ${esc(c.predicted.join(" + "))}</strong></div>`,
  )
  .join("");
renderQueue();
renderCase();
renderCounter();

$("integrity-case").innerHTML = integrity.cases
  .map(
    (c) =>
      `<option value="${esc(c.id)}" ${c.id === "cross_platform" ? "selected" : ""}>${esc(c.label)}</option>`,
  )
  .join("");
function renderIntegrity() {
  const c = integrity.cases.find(
    (item) => item.id === $("integrity-case").value,
  );
  $("integrity-result").innerHTML =
    `<div><span class="small-label">PROPOSED RECORD CHANGE</span><p>${esc(c.change)}</p></div><div><div class="decision">${badge(c.observed)}<strong>${c.observed === "rejected" ? "Stopped before tool output" : "Valid data, scoped conclusion"}</strong></div><p>${esc(c.reason)}</p>${c.result.readiness ? `<p class="boundary">Android readiness: <b>${esc(c.result.readiness.replaceAll("_", " "))}</b>. Acceptance of data does not mean launch approval.</p>` : ""}<details><summary>Inspect the recorded validation result</summary><pre>${esc(JSON.stringify(c.result, null, 2))}</pre></details></div>`;
}
$("integrity-case").addEventListener("change", renderIntegrity);
renderIntegrity();
