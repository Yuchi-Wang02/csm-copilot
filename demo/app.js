/* A transparent replay of Python outputs. No API, hidden AI, or simulated typing. */
"use strict";
const { workflow, evaluation: report, integrity, friction } = window.CSM_DATA;
const reviewLinks = window.CSM_REVIEW_LINKS;
const caseReview = window.CSM_CASE_REVIEW;
const copyFeedback = window.CSM_COPY_FEEDBACK.create();
const modelRuns = window.CSM_MODEL_RUNS;
const callbackProbes = window.CSM_DATA.callback_denial;
const practiceCases = window.CSM_PRACTICE.buildCases(window.CSM_DATA, modelRuns);
let { practiceId, invalid: practiceInvalid } = reviewLinks.readPractice(location.search, practiceCases);
let { probeId, invalid: probeInvalid } = reviewLinks.readProbe(location.search, callbackProbes.cases);
let { runId, invalid: runInvalid } = reviewLinks.readRun(location.search, modelRuns.runs);
let { selected, integration, activeTab, language, updated, verified, invalid } =
  reviewLinks.read(location.search, workflow);
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
      syncReviewUrl();
      document.querySelectorAll("[data-account]").forEach((item) => {
        const isSelected = Number(item.dataset.account) === selected;
        item.classList.toggle("active", isSelected);
        item.setAttribute("aria-pressed", String(isSelected));
      });
      renderCase();
    }),
  );
}
function checksTable(r) {
  return `<div class="decision">${badge(r.decision)}<strong>${esc(r.platform)} · scoped checklist</strong></div><table class="checks"><thead><tr><th>CHECK / SOURCE</th><th>STATE</th><th>EVIDENCE</th></tr></thead><tbody>${r.checks.map((c) => `<tr><td>${esc(c.label)}<a class="check-source" href="${esc(c.source_url)}" target="_blank" rel="noreferrer">${c.authority === "project_policy" ? "Project policy · related docs" : "Official documentation"} ↗</a></td><td>${badge(c.status)}</td><td>${c.evidence_ids.length ? c.evidence_ids.map((id) => `<span class="evidence-link">${esc(id)}</span>`).join("") : '<span class="evidence-link">No applicable record</span>'}</td></tr>`).join("")}</tbody></table><p class="boundary">${esc(r.boundary)}</p>`;
}
function renderCase() {
  // These controls are rebuilt below. Preserve the user's place only when
  // the replaced control held focus; other navigation keeps its own focus.
  const focusedControl = document.activeElement?.id;
  renderShareLink();
  const p = workflow.packets[selected],
    item = p.integrations[integration],
    r = item.readiness;
  $("case-download-label").textContent = `${r.app} / ${r.platform} brief`;
  for (const lang of ["en", "zh"]) {
    const link = $(`case-download-${lang}`);
    link.href = `case-briefs/${encodeURIComponent(r.integration_id)}-${lang}.md`;
    link.download = `csm-${r.integration_id}-${lang}.md`;
    link.setAttribute(
      "aria-label",
      `Download ${r.app} / ${r.platform} brief ${lang === "en" ? "in English" : "with Chinese drafts"}`,
    );
  }
  const records = caseReview.issuesFor(p, r.integration_id);
  const issueCount =
    records.length > 1
      ? `<p class="small-label">${records.length} recorded issues on this platform</p>`
      : "";
  $("account-heading").innerHTML =
    `<div><h3>${esc(p.selection.name)}</h3><p>${esc(r.app)} · ${esc(p.selection.stage)} · ${esc(p.selection.account_id)}</p></div><label><span class="small-label">PLATFORM </span><select id="platform-select" aria-label="Integration platform">${p.integrations.map((it, n) => `<option value="${n}" ${n === integration ? "selected" : ""}>${esc(it.readiness.platform)}</option>`).join("")}</select></label>`;
  $("platform-select").addEventListener("change", (e) => {
    integration = Number(e.target.value);
    syncReviewUrl();
    renderCase();
  });
  document.querySelectorAll("[data-tab]").forEach((b) => {
    b.setAttribute("aria-selected", String(b.dataset.tab === activeTab));
    b.tabIndex = b.dataset.tab === activeTab ? 0 : -1;
  });
  $("panel").setAttribute("aria-labelledby", `tab-${activeTab}`);
  if (activeTab === "evidence") {
    $("panel").innerHTML =
      issueCount +
      caseReview.evidenceHTML(records) +
      checksTable(r) +
      caseReview.readinessSourcesHTML(r, p.context) +
      caseReview.timingHTML(item.evidence_timing) +
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
      `<div class="toolbar"><label for="language-select">Client language</label><select id="language-select"><option value="en" ${language === "en" ? "selected" : ""}>English</option><option value="zh" ${language === "zh" ? "selected" : ""}>中文</option></select><button class="copy" id="copy-draft">Copy draft</button></div><div class="draft-purpose"><strong>Purpose: ${esc(draft.intent.replaceAll("_", " "))}</strong><p>${esc(draft.next_action)}</p></div><pre class="draft" lang="${language === "zh" ? "zh-CN" : "en"}">${esc(draft.body)}</pre><div class="notice"><b>DRAFT · NOT SENT</b> — Contact history is unchanged. Deterministic template; a host model may rewrite it with evidence-bound review.</div>${caseReview.followupSourcesHTML(draft, r, p.context)}<details><summary>Inspect draft provenance and review limits</summary><pre>${esc(JSON.stringify({ evidence_ids: draft.evidence_ids, issue_ids: draft.issue_ids, review: draft.review, requests: draft.requests }, null, 2))}</pre></details>`;
    $("language-select").addEventListener("change", (e) => {
      language = e.target.value;
      syncReviewUrl();
      renderCase();
    });
    $("copy-draft").addEventListener("click", (event) =>
      copyFeedback.copy(event.currentTarget, draft.body, "Copied", "Select text to copy"),
    );
  } else {
    $("panel").innerHTML =
      issueCount +
      caseReview.handoffHTML(records, item.followup_en.next_action);
  }
  if (["platform-select", "language-select"].includes(focusedControl)) {
    $(focusedControl)?.focus({ preventScroll: true });
  }
}
document.querySelectorAll("[data-tab]").forEach((b, n, buttons) => {
  b.addEventListener("click", () => {
    activeTab = b.dataset.tab;
    syncReviewUrl();
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
  const branch = verified ? "verified" : updated ? "after" : "before";
  const r = workflow.counterfactual[branch];
  $("counterfactual").innerHTML =
    `<span class="small-label">${verified ? "AFTER SYNTHETIC TEST RECORDS" : updated ? "AFTER CUSTOMER UPDATE" : "ORIGINAL EVIDENCE"}</span><div class="decision">${badge(r.decision)}<strong>Moon Garden / Android</strong></div>${r.checks
      .filter((c) =>
        ["currency_approved", "test_only_off", "device_verified", "callback_verified"].includes(
          c.id,
        ),
      )
      .map(
        (c) =>
          `<div class="counter-row"><span>${esc(c.label)}</span>${badge(c.status)}</div>`,
      )
      .join(
        "",
      )}<p style="margin-top:17px">${verified ? "All scoped checks are complete. The earlier reported issue remains recorded; ask whether it still occurs before discussing launch decisions." : updated ? "The settings are now customer-confirmed. The failed device check and missing callback verification remain unresolved." : "Two settings are unknown. A non-test device failure is already recorded."}</p>`;
  $("counterfactual").innerHTML += caseReview.timingHTML(
    workflow.counterfactual[`${branch}_timing`],
    ["currency_approved", "test_only_off", "device_verified", "callback_verified"],
    !verified,
  );
  if (verified) {
    const draft = workflow.counterfactual.verified_followup;
    $("counterfactual").innerHTML += `<div class="draft-purpose"><strong>Next action: ${esc(draft.intent.replaceAll("_", " "))}</strong><p>${esc(draft.next_action)}</p></div><pre class="draft">${esc(draft.body)}</pre><p class="notice">SYNTHETIC DRAFT · NOT SENT. The original workspace and downloads retain the original snapshot.</p><details><summary>Inspect the retained issue and test records</summary><pre>${esc(JSON.stringify({issues: workflow.counterfactual.verified_context.issues, evidence: workflow.counterfactual.verified_context.evidence.filter(e => ["reply_android_settings", "fresh_android_checks", ...draft.issue_ids.map(id => workflow.counterfactual.verified_context.issues.find(i => i.id === id).evidence_id)].includes(e.id))}, null, 2))}</pre></details>`;
  }
  $("verify-checks").disabled = !updated || verified;
  $("verify-checks").setAttribute("aria-pressed", String(verified));
  $("update-toggle").setAttribute("aria-pressed", String(updated));
  $("update-toggle").textContent = updated
    ? "Reset to original evidence ↺"
    : "Apply the synthetic customer update →";
}
$("update-toggle").addEventListener("click", () => {
  updated = !updated;
  verified = false;
  syncReviewUrl();
  renderShareLink();
  renderCounter();
});
$("verify-checks").addEventListener("click", () => {
  verified = true;
  syncReviewUrl();
  renderShareLink();
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

$("triage-probe").innerHTML = callbackProbes.cases.map((row) =>
  `<option value="${esc(row.id)}">${esc(row.kind === "known_limit" ? "Known limitation" : row.kind === "repair" ? "Repair probe" : "Positive control")} · ${esc(row.id.replaceAll("_", " "))}</option>`
).join("");
function renderTriageProbe() {
  $("triage-probe").value = probeId;
  $("share-probe-url").value = reviewLinks.shareProbe(probeId, callbackProbes.cases);
  copyFeedback.reset($("copy-probe-link"), "Copy this triage link");
  $("probe-route-notice").textContent = probeInvalid
    ? "The triage example in this link was invalid or ambiguous. The first published example is shown."
    : "";
  const row = callbackProbes.cases.find((c) => c.id === probeId);
  $("triage-probe-result").innerHTML = window.CSM_TRIAGE_REVIEW.render(row);
}
$("triage-probe").addEventListener("change", () => {
  probeId = $("triage-probe").value;
  syncReviewUrl("#triage-review");
  renderTriageProbe();
});
renderTriageProbe();

const trustBoundary = window.CSM_DATA.trust_boundary;
$("trust-probe").innerHTML = trustBoundary.cases
  .map((c) => `<option value="${esc(c.id)}">${esc(c.label)}</option>`).join("");
function renderTrustBoundary() {
  const row = trustBoundary.cases.find((c) => c.id === $("trust-probe").value);
  $("trust-result").innerHTML =
    `<p class="small-label">AUTHORED PROBE INPUT</p><blockquote>${esc(row.input)}</blockquote><h4>${esc(row.observed)}</h4><p>${esc(row.explanation)}</p><details><summary>Inspect the observed engine or parser result</summary><pre>${esc(JSON.stringify(row.result, null, 2))}</pre></details>`;
}
$("trust-probe").addEventListener("change", renderTrustBoundary);
renderTrustBoundary();

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

$("friction-scope").textContent =
  `Fixed snapshot: ${friction.as_of.slice(0, 10)} · ${friction.cohort_account_count} non-live accounts · ${friction.cohort_integration_count} integrations · all synthetic. Includes recently contacted accounts; this is broader than the morning queue.`;
$("friction-theme").innerHTML = friction.themes
  .map(
    (t) =>
      `<option value="${esc(t.check_id)}" ${t.check_id === "device_verified" ? "selected" : ""}>${esc(t.label)} — ${t.affected_account_count} ${t.affected_account_count === 1 ? "account" : "accounts"}</option>`,
  )
  .join("");
$("friction-counting").textContent =
  friction.counting_policy + " " + friction.recurrence_policy;
$("friction-boundary").textContent = friction.boundary;
function renderFriction() {
  const t = friction.themes.find(
    (item) => item.check_id === $("friction-theme").value,
  );
  if (!t) {
    $("friction-result").textContent =
      "No scoped checklist friction found. This does not establish that customers have no difficulties.";
    return;
  }
  $("friction-result").innerHTML =
    `<div class="friction-stats"><div><strong>${t.affected_account_count}</strong><span>${t.affected_account_count === 1 ? "distinct account" : "distinct accounts"}</span></div><div><strong>${t.affected_integration_count} / ${t.applicable_integration_count}</strong><span>affected / applicable integrations</span></div><div><strong>${t.unknown_integration_count}</strong><span>checks with unknown evidence</span></div><div><strong>${t.failed_integration_count}</strong><span>checks recorded as failed</span></div></div><p class="boundary">${t.recurring_across_accounts ? "Recurring across accounts in this snapshot." : "Single-account signal; recurrence across accounts is not established."} Counts overlap with other themes.</p><div class="friction-grid"><div class="friction-members">${t.members.map((m) => `<article><h3>${esc(m.account_name)}</h3><p>${esc(m.app)} / ${esc(m.platform)} · ${badge(m.status)}</p><p>${esc(m.next_question)}</p><details><summary>Inspect ${esc(m.integration_id)} evidence</summary>${m.source_records.length ? m.source_records.map((r) => `<p><b>${esc(r.id)}</b> · ${esc(r.at.slice(0, 10))}</p><p>${esc(r.text)}</p>`).join("") : "<p>No applicable record. This is a request for evidence, not a recorded failure.</p>"}</details></article>`).join("")}</div><aside class="friction-proposal"><span class="small-label">PROPOSED PRODUCT QUESTION</span><h3>${esc(t.product_question)}</h3><p><b>Proposed owner</b><br>${esc(t.proposed_owner)}</p><p><b>How to validate</b><br>${esc(t.validation_step)}</p><p class="boundary">${esc(t.interpretation)}</p><a href="${esc(t.source_url)}" target="_blank" rel="noopener noreferrer">Related product documentation ↗</a><p class="disclosure">Checklist authority: ${esc(t.rule_authority.replaceAll("_", " "))}. Product questions are project proposals.</p></aside></div>`;
}
$("friction-theme").addEventListener("change", renderFriction);
renderFriction();

$("model-run").innerHTML = modelRuns.runs
  .map(
    (r) =>
      `<option value="${esc(r.id)}">${esc(r.label)}</option>`,
  )
  .join("");
function renderModelRun() {
  $("model-run").value = runId;
  $("share-run-url").value = reviewLinks.shareRun(runId, modelRuns.runs);
  copyFeedback.reset($("copy-run-link"), "Copy this recording link");
  $("run-route-notice").textContent = runInvalid
    ? "The recording in this link was unknown or ambiguous. The latest published attempt is shown."
    : "";
  const run = modelRuns.runs.find((r) => r.id === runId);
  const trace = run.trace;
  const calls = trace.steps.flatMap(
    (s) => s.tool_calls || (s.tool_result ? [s] : []),
  );
  $("model-result").innerHTML =
    `<div class="model-verdict"><strong>${esc(run.verdict)}</strong><p>${esc(run.summary)}</p><span>${trace.coverage.observed} / ${trace.coverage.required} requested tool actions observed · ${esc(trace.model_id)} · ${esc(trace.runtime.device)}</span></div><details><summary>Read this attempt's task</summary><p>${esc(trace.task)}</p></details>${window.CSM_MODEL_TURNS.renderComparisons(run.claim_comparisons)}${window.CSM_MODEL_TURNS.render(trace)}<div class="model-grid"><div><h3>What the model actually did</h3>${calls.length ? `<ol class="model-calls">${calls.map((c) => `<li><code>${esc(c.action.tool)}</code><span>${esc(c.action.arguments.integration_id || c.action.arguments.account_id || c.action.arguments.issue_id || c.action.arguments.issue_text || "portfolio")} · ${c.tool_error ? "tool error" : "result received"}</span></li>`).join("")}</ol>` : "<p>No tool calls executed. Proposed actions in the raw output were rejected.</p>"}${renderResponseReview(run)}${run.display_final ? `<h3 class="model-final-title">Unedited model explanation · not verified</h3><p class="model-output">${esc(run.display_final)}</p><p class="boundary">Narrow promise lint: ${run.promise_lint.flags.length} flags. This lint does not verify whether the explanation matches the evidence.</p>` : ""}</div><aside class="model-review"><span class="small-label">SOURCE-BASED REVIEW</span>${run.findings.map((f) => `<div class="model-finding"><strong>${esc(f.kind)} · ${esc(f.claim)}</strong><p>${esc(f.assessment)}</p></div>`).join("")}<p class="disclosure">${esc(modelRuns.review_method)}.</p></aside></div><p class="boundary">${esc(modelRuns.boundary)}</p><a class="text-link" href="https://github.com/Yuchi-Wang02/csm-copilot/blob/main/evidence/model-runs/${esc(run.id)}.json">Complete trace, prompt and runtime settings ↗</a>`;
}
function selectModelRun(id) {
  runId = id;
  syncReviewUrl("#model-runs");
  renderModelRun();
}
$("model-run").addEventListener("change", (event) => selectModelRun(event.target.value));
renderModelRun();

function renderHandoffComparison() {
  const comparison = modelRuns.handoff_comparison;
  const [before, after] = comparison.attempts;
  const observations = [
    ["Requested actions observed", "required_actions"],
    ["Total attempted calls", "attempted_calls"],
    ["Tool errors", "tool_errors"],
    ["Triage input", "triage_input"],
    ["Triage result", "triage_result"],
  ];
  const table = (caption, rows) =>
    `<table><caption>${esc(caption)}</caption><thead><tr><th scope="col">Review point</th><th scope="col">Earlier run</th><th scope="col">With identifier check</th></tr></thead><tbody>${rows.map(([label, first, second]) => `<tr><th scope="row">${esc(label)}</th><td>${esc(first)}</td><td>${esc(second)}</td></tr>`).join("")}</tbody></table>`;
  $("model-comparison").innerHTML =
    `<p class="boundary">${esc(comparison.boundary)}</p><ul class="comparison-controls">${Object.entries(
      comparison.controls,
    )
      .map(
        ([label, same]) =>
          `<li><b>${esc(label)}:</b> ${same ? "same" : "different"}</li>`,
      )
      .join("")}</ul>` +
    table(
      "Recorded tool observations",
      observations.map(([label, key]) => [label, before[key], after[key]]),
    ) +
    table(
      "Explanation review · AI-assisted, not independent human validation",
      comparison.review_rows.map((row) => [row.label, row.before, row.after]),
    ) +
    `<p class="boundary">The newer answer handles some distinctions more clearly but loses the earlier evidence citation. Neither answer satisfies the complete task.</p><div class="comparison-actions"><button class="copy" data-compare-run="${esc(before.id)}">Inspect earlier recording</button><button class="copy" data-compare-run="${esc(after.id)}">Inspect recording with identifier check</button></div>`;
  document.querySelectorAll("[data-compare-run]").forEach((button) => {
    button.addEventListener("click", () => {
      selectModelRun(button.dataset.compareRun);
      $("model-result").focus({ preventScroll: true });
      $("model-result").scrollIntoView({ block: "start" });
    });
  });
}
renderHandoffComparison();

function renderResponseReview(run) {
  const review = run.trace.response_review;
  const corrections = run.trace.steps.filter((s) => s.correction_feedback);
  let html = corrections.length
    ? `<p class="boundary">${corrections.length} correction requests recorded. Original responses and exact feedback remain in the raw trace.</p>`
    : "";
  if (!review) return html;
  html += `<div class="structured-review"><h3>Structured field review</h3><strong>${esc(review.status.replaceAll("_", " "))}</strong><p>Free-form explanation: not semantically verified. Human review remains required.</p>${review.issues.length ? `<ul>${review.issues.map((i) => `<li>${esc(i.field)}: ${esc(i.code)}</li>`).join("")}</ul>` : "<p>The declared states and readiness source IDs match the observed tool outputs.</p>"}${review.checked_summary ? `<details><summary>Inspect system-rendered checked summary</summary><pre class="checked-summary">${esc(review.checked_summary)}</pre></details>` : ""}<p class="boundary">${esc(review.boundary)}</p></div>`;
  return html;
}

function reviewState() {
  return { selected, integration, activeTab, language, updated, verified };
}
function renderShareLink() {
  $("share-review-url").value = reviewLinks.share(reviewState(), workflow);
  copyFeedback.reset($("copy-review-link"), "Copy this review link");
  $("route-notice").textContent = invalid.length
    ? "Some review settings in this link were invalid or ambiguous. Default values are shown for those settings."
    : "";
}
function syncReviewUrl(anchor = location.hash || "#workspace") {
  invalid = [];
  runInvalid = false;
  probeInvalid = false;
  practiceInvalid = false;
  $("route-notice").textContent = "";
  $("run-route-notice").textContent = "";
  $("probe-route-notice").textContent = "";
  const runSetting = new URLSearchParams(location.search).has("run") || anchor === "#model-runs"
    ? "&" + reviewLinks.runQuery(runId, modelRuns.runs).slice(1)
    : "";
  const probeSetting = new URLSearchParams(location.search).has("probe") || anchor === "#triage-review"
    ? "&" + reviewLinks.probeQuery(probeId, callbackProbes.cases).slice(1)
    : "";
  const target =
    location.pathname +
    reviewLinks.query(reviewState(), workflow) +
    runSetting + probeSetting +
    (new URLSearchParams(location.search).has("practice") || anchor === "#practice"
      ? "&" + reviewLinks.practiceQuery(practiceId, practiceCases).slice(1) : "") + anchor;
  if (target !== location.pathname + location.search + location.hash) {
    try {
      history.pushState(null, "", target);
    } catch {
      /* File URLs can restrict history; the share link still works. */
    }
  }
  window.dispatchEvent(new CustomEvent("csm-practice-route", { detail: { practiceId, invalid: practiceInvalid } }));
}
function restoreReview(search = location.search) {
  ({ selected, integration, activeTab, language, updated, verified, invalid } =
    reviewLinks.read(search, workflow));
  ({ runId, invalid: runInvalid } = reviewLinks.readRun(search, modelRuns.runs));
  ({ probeId, invalid: probeInvalid } = reviewLinks.readProbe(search, callbackProbes.cases));
  ({ practiceId, invalid: practiceInvalid } = reviewLinks.readPractice(search, practiceCases));
  renderQueue();
  renderCase();
  renderCounter();
  renderModelRun();
  renderTriageProbe();
  window.dispatchEvent(new CustomEvent("csm-practice-route", { detail: { practiceId, invalid: practiceInvalid } }));
}
window.addEventListener("csm-practice-selection", (event) => {
  // The catalog validates the stable ID before it reaches browser history.
  reviewLinks.practiceQuery(event.detail, practiceCases);
  practiceId = event.detail;
  syncReviewUrl("#practice");
});
window.addEventListener("popstate", () => restoreReview());
// In-page evidence links preserve practice notes instead of reloading the document.
document.addEventListener("click", (event) => {
  const link = event.target.closest("a[data-review-link]");
  if (
    !link ||
    event.button !== 0 ||
    event.metaKey ||
    event.ctrlKey ||
    event.shiftKey ||
    event.altKey
  )
    return;
  if (!link.getAttribute("href").startsWith("?")) return;
  const target = new URL(link.href, location.href);
  if (
    target.origin !== location.origin ||
    target.pathname !== location.pathname
  )
    return;
  event.preventDefault();
  if (!target.searchParams.has("practice") && new URLSearchParams(location.search).has("practice"))
    target.searchParams.set("practice", practiceId);
  try {
    history.pushState(null, "", target.pathname + target.search + target.hash);
  } catch {
    /* File URLs may restrict history. */
  }
  restoreReview(target.search);
  const anchor = document.getElementById(target.hash.slice(1));
  if (anchor) {
    anchor.tabIndex = -1;
    anchor.focus({ preventScroll: true });
    anchor.scrollIntoView();
  }
});
$("copy-review-link").addEventListener("click", (event) => {
  const url = reviewLinks.share(reviewState(), workflow);
  return copyFeedback.copy(event.currentTarget, url, "Review link copied", "Select the link to copy", () => {
    $("review-link-details").open = true;
    $("share-review-url").focus();
    $("share-review-url").select();
  });
});
$("copy-run-link").addEventListener("click", (event) => {
  const url = reviewLinks.shareRun(runId, modelRuns.runs);
  return copyFeedback.copy(event.currentTarget, url, "Recording link copied", "Select the link to copy", () => {
    $("run-link-details").open = true;
    $("share-run-url").focus();
    $("share-run-url").select();
  });
});
$("copy-probe-link").addEventListener("click", (event) => {
  const url = reviewLinks.shareProbe(probeId, callbackProbes.cases);
  return copyFeedback.copy(event.currentTarget, url, "Triage link copied", "Select the link to copy", () => {
    $("probe-link-details").open = true;
    $("share-probe-url").focus();
    $("share-probe-url").select();
  });
});
