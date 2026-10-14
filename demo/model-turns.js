/* Explain recorded model/host/tool roles without replaying or changing actions. */
(function (root) {
  "use strict";
  const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (c) =>
    ({"&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"})[c]);
  const json = (value) => esc(JSON.stringify(value, null, 2));
  function outcome(step) {
    if (step.parse_error) return "Host rejected the proposed action";
    if (step.policy_error) return "Host rejected the dependency proposal";
    if (step.tool_calls?.some((c) => c.policy_result_error)) return "Host stopped after a result failed dependency checks";
    if (step.response_review?.status === "rejected") return "Host rejected the structured response";
    if (step.response_review?.status === "structured_fields_match") return "Structured fields matched; prose still needs review";
    if (step.tool_calls?.length) {
      const errors = step.tool_calls.filter((c) => c.tool_error).length;
      return `${step.tool_calls.length} recorded tool calls${errors ? ` · ${errors} tool ${errors === 1 ? "error" : "errors"}` : " · results received"}`;
    }
    if (step.actions?.some((a) => Object.hasOwn(a, "final"))) return "Model supplied a final response; prose unverified";
    return "Recorded model response";
  }
  function policyInputHTML(step, index) {
    if (!step.policy_message) return "";
    const state = step.policy_before || {};
    const pending = state.pending_actions?.length;
    const finalState = state.final_allowed === true ? "allowed" : state.final_allowed === false ? "not allowed" : "permission not recorded";
    return `<div class="turn-host"><h4>Host state supplied before this proposal</h4>` +
      `<p>The host supplied pending actions as planning assistance. This input is separate from the model's own proposal.</p>` +
      `<p>Stage: <code>${esc(state.stage)}</code> · ${esc(pending ?? "unknown")} pending ${pending === 1 ? "action" : "actions"} · Final response ${finalState}.</p>` +
      `<details><summary>Read the exact host state message</summary><p class="boundary">Recorded source: steps[${index}].policy_message</p><pre>${esc(step.policy_message.content)}</pre></details></div>`;
  }
  function turnHTML(step, index) {
    const calls = step.tool_calls || [];
    const actions = step.actions || [];
    const proposed = actions.filter((a) => a.tool);
    const finalAction = actions.find((a) => Object.hasOwn(a, "final"));
    const explanation = typeof finalAction?.final === "string"
      ? finalAction.final : finalAction?.final?.explanation;
    return `<li><details class="model-turn"><summary>Turn ${esc(step.number)} — ${esc(outcome(step))}</summary>` +
      `<p class="boundary">Recorded source: steps[${index}]. These are results from this attempt; current tools may differ.</p>` +
      policyInputHTML(step, index) +
      `<h4>Model proposal</h4>` +
      (proposed.length ? `<p>${proposed.length} proposed tool ${proposed.length === 1 ? "action" : "actions"}: ${proposed.map((a) => `<code>${esc(a.tool)}</code>`).join(", ")}.</p>` : "") +
      (typeof explanation === "string" ? `<p class="model-output">${esc(explanation)}</p><p class="boundary">Model-written explanation from the parsed final response; not verified.</p>` : "") +
      `<details><summary>Read the unedited model output for this turn</summary><pre>${esc(step.model_response?.text ?? "No model text recorded.")}</pre></details>` +
      (step.parse_error ? `<div class="turn-host"><h4>Host action validation</h4><p>${esc(step.parse_error)}</p><p>No tool calls were executed in this turn.</p></div>` : "") +
      (step.policy_error ? `<div class="turn-host"><h4>Host dependency validation</h4><p>${esc(step.policy_error)}</p><p>The whole proposal was rejected before tool execution.</p></div>` : "") +
      (calls.length ? `<h4>Tool execution through MCP</h4><ol class="turn-calls">${calls.map((call, callIndex) =>
        `<li><strong>${esc(call.action.tool)}</strong><span>${call.tool_error ? "Tool error" : "Result received"}${call.action.arguments.integration_id || call.action.arguments.issue_id || call.action.arguments.account_id ? ` · requested ID: ${esc(call.action.arguments.integration_id || call.action.arguments.issue_id || call.action.arguments.account_id)}` : ""}</span><details><summary>Inspect call ${callIndex + 1} · ${esc(call.action.tool)}</summary><h5>Arguments supplied by the model</h5><pre>${json(call.action.arguments)}</pre><h5>${call.tool_error ? "Recorded error response" : "Recorded tool result"}</h5><pre>${json(call.tool_result)}</pre>${call.policy_after ? `<h5>Host dependency state after this result</h5><pre>${json(call.policy_after)}</pre>` : ""}${call.policy_result_error ? `<h5>Host rejected this result for workflow progress</h5><p>${esc(call.policy_result_error)}</p><p>Later actions in this batch were not executed.</p>` : ""}</details></li>`
      ).join("")}</ol>` : "") +
      (step.response_review ? `<div class="turn-host"><h4>Host structured-field review</h4><p>Status: <code>${esc(step.response_review.status)}</code>. Free-text verification: <code>${esc(step.response_review.free_text_verification)}</code>.</p><p>${esc(step.response_review.boundary)}</p><details><summary>Inspect the field checks for this turn</summary><pre>${json(step.response_review)}</pre></details></div>` : "") +
      (step.correction_feedback ? `<div class="turn-correction"><h4>Host correction request ${esc(step.repair_number)}</h4><p>The host supplied this feedback for the next model turn. It may include expected values; this is assisted recovery.</p><pre>${esc(step.correction_feedback.content)}</pre></div>` : "") +
      `</details></li>`;
  }
  function render(trace) {
    return `<section class="model-conversation"><h3>How this recorded AI run unfolded</h3>` +
      `<p>The <strong>model</strong> proposes tool calls and writes a response. The <strong>host</strong> validates actions and can request corrections. The <strong>MCP tools</strong> return scoped evidence and drafts. A <strong>human</strong> still reviews the result.</p>` +
      `<p class="boundary">Recorded terminal status: <code>${esc(trace.status)}</code>. This view reads the saved conversation; it performs no inference or tool calls.</p>` +
      `<details><summary>Read the initial model instructions and task</summary>${(trace.initial_messages || []).map((m) => `<h4>Recorded ${esc(m.role)} message</h4><pre>${esc(m.content)}</pre>`).join("")}</details>` +
      `<ol class="model-turns">${trace.steps.map(turnHTML).join("")}</ol>` +
      `<details><summary>Inspect raw model turns and tool results</summary><pre>${json(trace.steps)}</pre></details></section>`;
  }
  function renderComparisons(rows) {
    if (!rows?.length) return "";
    return `<section class="claim-comparison"><h3>Check the claim against the recorded result</h3>` +
      `<p>Two excerpts from this attempt's final answer, paired with the tool fields available to the model.</p>` +
      rows.map((row) => `<div class="claim-pair"><div><span class="small-label">MODEL EXCERPT · UNVERIFIED</span><blockquote>${esc(row.claim)}</blockquote><p>${esc(row.assessment)}</p></div>` +
        `<div><span class="small-label">RECORDED TOOL FIELDS</span><p class="claim-source">${esc(row.source_label)}</p><dl>${row.fields.map((field) => `<dt>${esc(field.label)}</dt><dd>${esc(typeof field.value === "string" ? field.value : JSON.stringify(field.value))}</dd>`).join("")}</dl>` +
        `<details><summary>Locate these fields in the raw trace</summary>${row.fields.map((field) => `<p>${esc(field.label)}<br><code>${esc(field.path)}</code></p>`).join("")}</details></div></div>`).join("") +
      `<p class="boundary">AI-assisted review of a saved attempt, not an automated semantic verdict. These are historical tool returns; current tools and the underlying source truth are separate questions.</p></section>`;
  }
  const api = { render, renderComparisons };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CSM_MODEL_TURNS = api;
})(typeof window !== "undefined" ? window : this);
