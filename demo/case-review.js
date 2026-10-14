/* Keep every scoped issue paired with its own source and handoff. */
(function (root) {
  "use strict";
  const esc = (value) =>
    String(value ?? "").replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  const badge = (status) =>
    `<span class="badge ${esc(status)}">${esc(status.replaceAll("_", " "))}</span>`;
  const sourceLabel = (kind) => kind === "customer_report" ? "Customer report" : kind === "test_record" ? "Test record" : "Source type unavailable";
  const sourceDisclosure = (kind) => kind === "customer_report" ? "Read original customer message" : kind === "test_record" ? "Read original test record" : "Read original issue record";

  function issuesFor(packet, integrationId) {
    return packet.context.issues
      .filter((issue) => issue.integration_id === integrationId)
      .map((issue) => ({
        issue,
        evidence: packet.context.evidence.find(
          (record) =>
            record.id === issue.evidence_id &&
            record.integration_id === integrationId,
        ),
        ticket: packet.tickets.find(
          (ticket) => ticket.draft_id === `ticket-${issue.id}`,
        ),
      }));
  }

  function evidenceHTML(records) {
    if (!records.length)
      return '<div class="quote"><p>No issue message recorded for this integration. Readiness still depends on its own evidence.</p></div>';
    return records
      .map(
        ({ issue, evidence }) =>
          `<article class="quote issue-review"><p>${esc(issue.summary)}</p>` +
          (evidence
            ? `<details><summary>${sourceDisclosure(evidence.kind)} · ${esc(issue.id)}</summary><p lang="${evidence.language === "zh" ? "zh-CN" : "en"}">${esc(evidence.text)}</p></details><small>${sourceLabel(evidence.kind)} · ${esc(evidence.id)} · ${esc(evidence.at.slice(0, 10))}</small>`
            : `<p class="boundary">Source record unavailable for ${esc(issue.id)}. Do not infer the original message from its summary.</p>`) +
          "</article>",
      )
      .join("");
  }

  function candidateHTML(candidate) {
    const source = candidate.source_url;
    let link = "";
    if (source) {
      let valid = false;
      try { valid = new URL(source).protocol === "https:"; } catch { /* Show invalid sources as text. */ }
      link = valid
        ? `<a href="${esc(source)}" target="_blank" rel="noopener noreferrer">Related documentation ↗</a>`
        : `<p class="boundary">Source URL unavailable as a safe link: ${esc(source)}</p>`;
    }
    return `<section class="handoff-candidate"><h4>${candidate.category === "unknown" ? "Clarify the request" : `Candidate: ${esc(candidate.category.replaceAll("_", " "))}`}</h4><ul>${candidate.questions.map((q) => `<li>${esc(q)}</li>`).join("")}</ul>${link}</section>`;
  }

  function ticketHTML({ issue, evidence, ticket: t }) {
    if (!t)
      return `<article class="issue-review"><h3>${esc(issue.summary)}</h3><p class="boundary">Handoff draft unavailable for ${esc(issue.id)}. The issue is recorded; review its source before preparing a draft.</p></article>`;
    const fieldStatus =
      t.handoff_state === "needs_scope"
        ? "<strong>Clarify the request first</strong>Generic field completeness does not establish issue scope. Confirm the request, desired outcome and relevant account or product before choosing an owner or requesting technical details."
        : `<strong>${t.missing_fields.length ? "Request before technical review" : "Ready for handoff review"}</strong>${t.missing_fields.length ? t.missing_fields.map((f) => `<code>${esc(f)}</code>`).join(" ") : "All scoped required fields are present. Confirm their content and the appropriate owner before submission."}`;
    return (
      `<article class="issue-review"><h3>${esc(t.title)}</h3><div class="decision">${badge(t.handoff_state)}<strong>Root cause: ${esc(t.root_cause)}</strong></div>` +
      `<dl class="ticket-fields">${Object.entries(t.fields)
        .map(
          ([key, value]) =>
            `<dt>${esc(key.replaceAll("_", " "))}</dt><dd>${esc(value)}</dd>`,
        )
        .join(
          "",
        )}<dt>Evidence</dt><dd>${esc(t.evidence_ids.join(", "))}</dd><dt>Suggested owner</dt><dd>${esc(t.suggested_owner)}</dd></dl>` +
      `<div class="missing">${fieldStatus}</div><p class="boundary">${esc(t.next_action)}</p>` +
      (t.collection_requests?.length
        ? `<section class="handoff-questions"><h3>Request missing intake details</h3><ul>${t.collection_requests.map((r) => `<li>${esc(r.request)}</li>`).join("")}</ul></section>`
        : "") +
      (t.collection_boundary ? `<p class="boundary">${esc(t.collection_boundary)}</p>` : "") +
      (evidence
        ? `<details><summary>Original issue record · ${esc(evidence.id)}</summary><p class="boundary">${sourceLabel(evidence.kind)} · ${esc(evidence.at)}</p><p lang="${evidence.language === "zh" ? "zh-CN" : "en"}">${esc(evidence.text)}</p></details>`
        : '<p class="boundary">Original issue record unavailable for this platform.</p>') +
      `<details class="handoff-questions"${t.handoff_state === "needs_scope" ? " open" : ""}><summary>Questions to review before handoff</summary><p class="boundary">Broader suggestions from lexical triage. Some details may already be recorded above; these do not establish a root cause. Review the original report before requesting additional evidence.</p>${(t.triage.candidates || []).map(candidateHTML).join("") || '<p>No candidate questions recorded.</p>'}</details>` +
      t.triage.notes.map((note) => `<p class="boundary">${esc(note)}</p>`).join("") +
      `<details><summary>Inspect candidate checks and source URLs · ${esc(issue.id)}</summary><pre>${esc(JSON.stringify(t.triage, null, 2))}</pre></details>` +
      `<details><summary>Trace each handoff field to its record · ${esc(issue.id)}</summary><pre>${esc(JSON.stringify(t.field_sources, null, 2))}</pre></details></article>`
    );
  }

  function handoffHTML(records, nextAction) {
    if (!records.length)
      return `<div class="empty"><h3>No recorded issue to escalate.</h3><p>${esc(nextAction)}</p><p class="boundary">A readiness unknown does not automatically become a support ticket.</p></div>`;
    return records.map(ticketHTML).join("");
  }
  function timingHTML(timing, checkIds = null, expanded = false) {
    const relevant = (ids) => checkIds ? ids.filter((id) => checkIds.includes(id)) : ids;
    const records = timing.records.filter((record) => relevant(record.check_ids).length);
    return `<details class="evidence-timing" ${expanded ? "open" : ""}><summary>Evidence timing · ${records.length} supporting ${records.length === 1 ? "record" : "records"}</summary><p class="boundary">Snapshot: ${esc(timing.as_of)}</p>` +
      (records.length ? `<ol>${records.map((record) => `<li><strong>${esc(record.id)}</strong><span>${esc(record.kind.replaceAll("_", " "))} · ${esc(record.age_days.toFixed(2))} days before snapshot</span><time datetime="${esc(record.recorded_at)}">${esc(record.recorded_at)}</time><small>Supports: ${esc(relevant(record.check_ids).join(", "))}</small></li>`).join("")}</ol>` : '<p>No available supporting records for these checks.</p>') +
      (timing.unavailable_ids.length ? `<p class="notice">Unavailable scoped sources: ${esc(timing.unavailable_ids.join(", "))}</p>` : "") +
      `<p class="boundary">${esc(timing.boundary)}</p></details>`;
  }
  const api = { issuesFor, evidenceHTML, handoffHTML, timingHTML };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CSM_CASE_REVIEW = api;
})(typeof window !== "undefined" ? window : this);
