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
            ? `<details><summary>Read original customer message · ${esc(issue.id)}</summary><p lang="${evidence.language === "zh" ? "zh-CN" : "en"}">${esc(evidence.text)}</p></details><small>CUSTOMER REPORT · ${esc(evidence.id)} · ${esc(evidence.at.slice(0, 10))}</small>`
            : `<p class="boundary">Source record unavailable for ${esc(issue.id)}. Do not infer the original message from its summary.</p>`) +
          "</article>",
      )
      .join("");
  }

  function ticketHTML({ issue, ticket: t }) {
    if (!t)
      return `<article class="issue-review"><h3>${esc(issue.summary)}</h3><p class="boundary">Handoff draft unavailable for ${esc(issue.id)}. The issue is recorded; review its source before preparing a draft.</p></article>`;
    const fieldStatus =
      t.handoff_state === "needs_scope"
        ? "<strong>Clarify the request first</strong>Generic field completeness does not establish issue scope. Confirm what happened and what was expected before choosing an owner or requesting technical details."
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
      `<div class="missing">${fieldStatus}</div><p class="boundary">${esc(t.next_action)}</p>${t.triage.notes.map((note) => `<p class="boundary">${esc(note)}</p>`).join("")}` +
      `<details><summary>Inspect candidate checks and source URLs · ${esc(issue.id)}</summary><pre>${esc(JSON.stringify(t.triage, null, 2))}</pre></details>` +
      `<details><summary>Trace each handoff field to its record · ${esc(issue.id)}</summary><pre>${esc(JSON.stringify(t.field_sources, null, 2))}</pre></details></article>`
    );
  }

  function handoffHTML(records, nextAction) {
    if (!records.length)
      return `<div class="empty"><h3>No recorded issue to escalate.</h3><p>${esc(nextAction)}</p><p class="boundary">A readiness unknown does not automatically become a support ticket.</p></div>`;
    return records.map(ticketHTML).join("");
  }
  const api = { issuesFor, evidenceHTML, handoffHTML };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CSM_CASE_REVIEW = api;
})(typeof window !== "undefined" ? window : this);
