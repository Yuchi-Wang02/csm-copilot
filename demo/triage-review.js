/* Render preserved development probes; this module never runs a model or triage. */
(function (root) {
  "use strict";
  const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);
  const same = (left, right) => JSON.stringify([...new Set(left)].sort()) === JSON.stringify([...new Set(right)].sort());
  const names = (categories) => categories.map((c) => esc(c.replaceAll("_", " "))).join(" + ");
  function render(row) {
    const matches = same(row.after, row.expected), changed = !same(row.before, row.after);
    const status = !matches ? "Still differs from project expectation" : changed ? "Changed; matches project expectation" : "Unchanged; matches project expectation";
    return `<p class="small-label">${esc(row.id)} · inspected development probe</p>` +
      `<blockquote>${esc(row.text)}</blockquote>` +
      `<div class="triage-comparison"><div><h4>Before repair</h4><p>${names(row.before)}</p></div><div><h4>Current categories</h4><p>${names(row.after)}</p></div><div><h4>Project expectation</h4><p>${names(row.expected)}</p></div></div>` +
      `<p class="triage-status ${matches ? "matches" : "differs"}" role="status">${status}</p>` +
      `<p><strong>Current route:</strong> ${esc(row.after_result.route.replaceAll("_", " "))}. <strong>Root cause:</strong> ${esc(row.after_result.root_cause)}.</p>` +
      (row.after_result.notes.length ? `<ul>${row.after_result.notes.map((note) => `<li>${esc(note)}</li>`).join("")}</ul>` : '<p class="boundary">No exclusion note was returned for this message.</p>') +
      `<details><summary>Inspect the preserved before-repair tool result</summary><pre>${esc(JSON.stringify(row.before_result, null, 2))}</pre></details>` +
      `<details><summary>Inspect this recorded current tool result</summary><pre>${esc(JSON.stringify(row.after_result, null, 2))}</pre></details>`;
  }
  const api = { render };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CSM_TRIAGE_REVIEW = api;
})(typeof window !== "undefined" ? window : this);
