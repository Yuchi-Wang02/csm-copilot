/* A transparent replay of Python outputs. No API, hidden AI, or simulated typing. */
"use strict";
const { workflow, evaluation: report, integrity, friction } = window.CSM_DATA;
const reviewLinks = window.CSM_REVIEW_LINKS;
let { selected, integration, activeTab, language, updated, invalid } =
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
      renderQueue();
      renderCase();
    }),
  );
}
function checksTable(r) {
  return `<div class="decision">${badge(r.decision)}<strong>${esc(r.platform)} · scoped checklist</strong></div><table class="checks"><thead><tr><th>CHECK / SOURCE</th><th>STATE</th><th>EVIDENCE</th></tr></thead><tbody>${r.checks.map((c) => `<tr><td>${esc(c.label)}<a class="check-source" href="${esc(c.source_url)}" target="_blank" rel="noreferrer">${c.authority === "project_policy" ? "Project policy · related docs" : "Official documentation"} ↗</a></td><td>${badge(c.status)}</td><td>${c.evidence_ids.length ? c.evidence_ids.map((id) => `<span class="evidence-link">${esc(id)}</span>`).join("") : '<span class="evidence-link">No applicable record</span>'}</td></tr>`).join("")}</tbody></table><p class="boundary">${esc(r.boundary)}</p>`;
}
function renderCase() {
  renderShareLink();
  const p = workflow.packets[selected],
    item = p.integrations[integration],
    r = item.readiness;
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
      syncReviewUrl();
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
        `<div class="empty"><h3>No recorded issue to escalate.</h3><p>${esc(item.followup_en.next_action)}</p><p class="boundary">A readiness unknown does not automatically become a support ticket.</p></div>`;
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

const modelRuns = window.CSM_MODEL_RUNS;
$("model-run").innerHTML = modelRuns.runs
  .map(
    (r) =>
      `<option value="${esc(r.id)}" ${r.id === modelRuns.runs.at(-1).id ? "selected" : ""}>${esc(r.label)}</option>`,
  )
  .join("");
function renderModelRun() {
  const run = modelRuns.runs.find((r) => r.id === $("model-run").value);
  const trace = run.trace;
  const calls = trace.steps.flatMap(
    (s) => s.tool_calls || (s.tool_result ? [s] : []),
  );
  $("model-result").innerHTML =
    `<div class="model-verdict"><strong>${esc(run.verdict)}</strong><p>${esc(run.summary)}</p><span>${trace.coverage.observed} / ${trace.coverage.required} requested tool actions observed · ${esc(trace.model_id)} · ${esc(trace.runtime.device)}</span></div><div class="model-grid"><div><h3>What the model actually did</h3>${calls.length ? `<ol class="model-calls">${calls.map((c) => `<li><code>${esc(c.action.tool)}</code><span>${esc(c.action.arguments.integration_id || "")} · ${c.tool_error ? "tool error" : "result received"}</span></li>`).join("")}</ol>` : "<p>No tool calls executed. Proposed actions in the raw output were rejected.</p>"}<details><summary>Inspect raw model turns and tool results</summary><pre>${esc(JSON.stringify(trace.steps, null, 2))}</pre></details>${renderResponseReview(run)}${run.display_final ? `<h3 class="model-final-title">Unedited model explanation · not verified</h3><p class="model-output">${esc(run.display_final)}</p><p class="boundary">Narrow promise lint: ${run.promise_lint.flags.length} flags. This lint does not verify whether the explanation matches the evidence.</p>` : ""}</div><aside class="model-review"><span class="small-label">SOURCE-BASED REVIEW</span>${run.findings.map((f) => `<div class="model-finding"><strong>${esc(f.kind)} · ${esc(f.claim)}</strong><p>${esc(f.assessment)}</p></div>`).join("")}<p class="disclosure">${esc(modelRuns.review_method)}.</p></aside></div><p class="boundary">${esc(modelRuns.boundary)}</p><a class="text-link" href="https://github.com/Yuchi-Wang02/csm-copilot/blob/main/evidence/model-runs/${esc(run.id)}.json">Complete trace, prompt and runtime settings ↗</a>`;
}
$("model-run").addEventListener("change", renderModelRun);
renderModelRun();

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
  return { selected, integration, activeTab, language, updated };
}
function renderShareLink() {
  $("share-review-url").value = reviewLinks.share(reviewState(), workflow);
  $("copy-review-link").textContent = "Copy this review link";
  $("route-notice").textContent = invalid.length
    ? "Some review settings in this link were invalid or ambiguous. Default values are shown for those settings."
    : "";
}
function syncReviewUrl() {
  invalid = [];
  const target =
    location.pathname +
    reviewLinks.query(reviewState(), workflow) +
    (location.hash || "#workspace");
  if (target !== location.pathname + location.search + location.hash) {
    try {
      history.pushState(null, "", target);
    } catch {
      /* File URLs can restrict history; the share link still works. */
    }
  }
}
function restoreReview(search = location.search) {
  ({ selected, integration, activeTab, language, updated, invalid } =
    reviewLinks.read(search, workflow));
  renderQueue();
  renderCase();
  renderCounter();
}
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
$("copy-review-link").addEventListener("click", async () => {
  const url = reviewLinks.share(reviewState(), workflow);
  try {
    await navigator.clipboard.writeText(url);
    $("copy-review-link").textContent = "Review link copied";
  } catch {
    $("review-link-details").open = true;
    $("share-review-url").focus();
    $("share-review-url").select();
    $("copy-review-link").textContent = "Select the link to copy";
  }
});
