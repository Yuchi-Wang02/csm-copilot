/* Explain recorded model/host/tool roles without replaying or changing actions. */
(function (root) {
  "use strict";
  const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (c) =>
    ({"&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"})[c]);
  const json = (value) => esc(JSON.stringify(value, null, 2));
  function outcome(step) {
    if (!step.model_response && step.request_state) {
      return ({prepared: "Request prepared; dispatch not confirmed", sent: "Request sent; response not recorded",
        response_timeout: "Worker response timed out; no response recorded", response_error: "Worker response failed",
        cancelled: "Request interrupted by cancellation", host_error: "Host failed during request handling"})[step.request_state] || "Request recorded; response not recorded";
    }
    if (step.parse_error) return "Host rejected the proposed action";
    if (step.policy_error) return "Host rejected the dependency proposal";
    if (step.tool_calls?.some((c) => c.policy_result_error)) return "Host stopped after a result failed dependency checks";
    if (step.response_review?.status === "rejected") return "Host rejected the structured response";
    if (step.response_review?.status === "structured_fields_match") return "Structured fields matched; prose still needs review";
    if (step.tool_calls?.length) {
      const errors = step.tool_calls.filter((c) => c.tool_error).length;
      return `${step.tool_calls.length} recorded tool ${step.tool_calls.length === 1 ? "call" : "calls"}${errors ? ` · ${errors} tool ${errors === 1 ? "error" : "errors"}` : " · results received"}`;
    }
    if (step.actions?.some((a) => Object.hasOwn(a, "final"))) return "Model supplied a final response; prose unverified";
    return "Recorded model response";
  }
  function requestHTML(step, index) {
    if (!step.worker_request) return "";
    return `<div class="turn-host"><h4>Recorded worker request</h4>` +
      `<p>Request state: <code>${esc(step.request_state)}</code> · Response budget: ${esc(step.response_timeout_seconds)} seconds. Sent means written to the worker pipe, not acknowledged by the model.</p>` +
      `<details><summary>Inspect the exact saved worker input</summary><p class="boundary">Recorded source: steps[${index}].worker_request · SHA-256: <code>${esc(step.request_sha256)}</code> · Encoding: ${esc(step.request_encoding)}</p><pre>${json(step.worker_request)}</pre></details>` +
      (step.response_error ? `<h4>Worker response failure</h4><p><code>${esc(step.response_error.type)}</code>: ${esc(step.response_error.message || "No error message supplied")}</p><p>No usable response was recorded for this request. Partial output captured: <code>${esc(step.response_error.partial_output_captured)}</code>.</p>` : "") +
      (step.failure_phase ? `<p>Failure phase: <code>${esc(step.failure_phase)}</code>. A dispatch failure does not establish whether the worker received any bytes.</p>` : "") +
      (typeof step.worker_response_text === "string" ? `<details><summary>Inspect the invalid worker envelope</summary><p>This line could not be decoded as JSON; it is not an accepted model response.</p><pre>${esc(step.worker_response_text)}</pre></details>` : "") +
      `</div>`;
  }
  function policyInputHTML(step, index) {
    if (!step.policy_message) return "";
    const state = step.policy_before || {};
    const pending = state.pending_actions?.length;
    const finalState = state.final_allowed === true ? "allowed" : state.final_allowed === false ? "not allowed" : "permission not recorded";
    return `<div class="turn-host"><h4>${step.model_response ? "Host state supplied before this proposal" : "Host state supplied with this request"}</h4>` +
      `<p>The host supplied pending actions as planning assistance. This input is separate from model-generated output.</p>` +
      `<p>Stage: <code>${esc(state.stage)}</code> · ${esc(pending ?? "unknown")} pending ${pending === 1 ? "action" : "actions"} · Final response ${finalState}.</p>` +
      `<details><summary>Read the exact host state message</summary><p class="boundary">Recorded source: steps[${index}].policy_message</p><pre>${esc(step.policy_message.content)}</pre></details></div>`;
  }
  function generationSchemaHTML(step, index) {
    if (!step.generation_schema) return "";
    return `<div class="turn-host"><h4>Host requested constrained generation</h4>` +
      `<p>The host supplied a JSON schema to restrict generated output. This is decoding assistance; it does not verify factual claims.</p>` +
      (step.model_response?.schema_constrained === true ? `<p>The model worker reported schema-constrained generation for this turn.</p>` : step.model_response ? `<p>The recorded response does not confirm that the decoding constraint was active.</p>` : `<p>No response is available to confirm that the decoding constraint was active.</p>`) +
      `<details><summary>Inspect the generation schema</summary><p class="boundary">Recorded source: steps[${index}].generation_schema</p><pre>${json(step.generation_schema)}</pre></details></div>`;
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
      requestHTML(step, index) +
      (step.context_reduction ? `<div class="turn-host"><h4>Final context reduction</h4><p>The host retained ${esc(step.context_reduction.retained_message_count)} of ${esc(step.context_reduction.original_message_count)} messages in this worker request.</p><p class="boundary">${esc(step.context_reduction.boundary)}</p><details><summary>Inspect omitted host messages and original positions</summary><p class="boundary">Recorded source: steps[${index}].context_reduction</p><pre>${json(step.context_reduction)}</pre></details></div>` : "") +
      policyInputHTML(step, index) +
      (step.explanation_guidance_message ? `<div class="turn-host"><h4>Host explanation checklist</h4><p>The host supplied an optional writing checklist after tool work. This is prompt assistance, not model reasoning or verification of its explanation.</p><details><summary>Read the exact explanation guidance</summary><p class="boundary">Recorded source: steps[${index}].explanation_guidance_message</p><pre>${esc(step.explanation_guidance_message.content)}</pre></details></div>` : "") +
      (step.final_contract_message ? `<div class="turn-host"><h4>Host final-answer contract</h4><p>The host supplied the required final fields after tool work. These instructions are assistance, not model-written reasoning.</p><details><summary>Read the exact final contract message</summary><p class="boundary">Recorded source: steps[${index}].final_contract_message</p><pre>${esc(step.final_contract_message.content)}</pre></details></div>` : "") +
      generationSchemaHTML(step, index) +
      (step.model_response ? `<h4>Model proposal</h4>` : `<h4>No model response recorded</h4>`) +
      (proposed.length ? `<p>${proposed.length} proposed tool ${proposed.length === 1 ? "action" : "actions"}: ${proposed.map((a) => `<code>${esc(a.tool)}</code>`).join(", ")}.</p>` : "") +
      (typeof explanation === "string" ? `<p class="model-output">${esc(explanation)}</p><p class="boundary">Model-written explanation from the parsed final response; not verified.</p>` : "") +
      (step.model_response ? `<details><summary>Read the unedited model output for this turn</summary><pre>${esc(step.model_response.text ?? "No model text recorded.")}</pre></details>` : `<p>No model proposal or final answer is inferred from the saved request.</p>`) +
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
      (trace.error_type ? `<p class="boundary">Recorded host error type: <code>${esc(trace.error_type)}</code>. See the attempt review for the terminal observation and limits of the saved trace.</p>` : "") +
      (trace.error_causes?.length ? `<details><summary>Inspect recorded failure causes</summary><pre>${json(trace.error_causes)}</pre></details>` : "") +
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
  function renderCorrectionComparison(comparison) {
    if (!comparison) return "";
    const same = (row) => JSON.stringify(row.before) === JSON.stringify(row.after);
    const value = (data, other) => Array.isArray(data)
      ? `<ul>${data.map((item) => `<li><code>${esc(item)}</code>${other && !other.includes(item) ? ' <strong class="removed-citation">Removed in correction</strong>' : ""}</li>`).join("")}</ul>`
      : `<p class="correction-prose">${esc(data)}</p>`;
    return `<section class="correction-comparison"><h3>What changed after the correction?</h3>` +
      `<p>Compare the saved model answers: turn ${esc(comparison.before_turn)} was rejected; turn ${esc(comparison.after_turn)} matched the checked fields. The host supplied expected values between them.</p>` +
      comparison.rows.map((row) => `<div class="correction-row"><h4>${esc(row.label)}</h4>` +
        (same(row) ? `<span class="small-label">UNCHANGED IN BOTH ANSWERS</span>${value(row.before)}` :
          `<div class="correction-values"><div><span class="small-label">BEFORE · TURN ${esc(comparison.before_turn)}</span>${value(row.before, row.after)}</div><div><span class="small-label">AFTER · TURN ${esc(comparison.after_turn)}</span>${value(row.after)}</div></div>`) + `</div>`).join("") +
      `<details><summary>Read the exact correction feedback</summary><p class="claim-source">${esc(comparison.feedback_path)}</p><pre>${esc(comparison.feedback.content)}</pre></details>` +
      `<details><summary>Locate the compared fields in the raw trace</summary>${comparison.rows.map((row) => `<h4>${esc(row.label)}</h4>${row.paths.map((path) => `<p><code>${esc(path)}</code></p>`).join("")}`).join("")}</details>` +
      `<p class="boundary">${esc(comparison.boundary)}</p></section>`;
  }
  function renderMorningComparison(runs) {
    const morning = runs.filter((run) => run.trace?.task_id === "morning_review");
    if (!morning.length) return "";
    const flag = (value) => value === true ? "Enabled" : value === false ? "Disabled" : "Not recorded";
    const recorded = (value, unit = "") => value === undefined || value === null ? "Not recorded" : `${esc(value)}${unit}`;
    const rows = morning.map((run) => {
      const t = run.trace, c = t.coverage || {};
      const settings = [
        ["Dependency policy", flag(t.enforce_dependencies)],
        ["Constrained actions", flag(t.constrain_actions)],
        ["Morning final-field review", flag(t.review_morning_final)],
        ["Reduced final context", flag(t.compact_final_context)],
        ["Explanation checklist", flag(t.explanation_checklist)],
        ["Output-token cap", recorded(t.runtime?.max_new_tokens)],
        ["Response wait budget", recorded(t.response_timeout_seconds, " seconds")],
        ["Correction budget", recorded(t.repair_budget)],
      ];
      const final = c.final_response_present === true ? "Final response recorded" : c.final_response_present === false ? "No final response recorded" : "Final-response presence not recorded";
      const unique = typeof run.id === "string" && /^[a-z0-9-]+$/.test(run.id) && runs.filter((r) => r.id === run.id).length === 1;
      const link = unique ? `<a data-review-link href="?run=${encodeURIComponent(run.id)}#model-result" aria-label="Inspect recording: ${esc(run.label)}">Inspect recording →</a>` : "Recording link unavailable";
      return `<tr><th scope="row">${esc(run.label)}<details><summary>Recorded setup</summary><dl>${settings.map(([label, value]) => `<dt>${label}</dt><dd>${value}</dd>`).join("")}</dl><p class="disclosure">Absent fields are not treated as disabled. Inspect the original instructions and schemas in the recording.</p></details></th>` +
        `<td><strong>${recorded(c.observed)} / ${recorded(c.required)} requested actions observed</strong><p>${final}</p><p>Host status: <code>${esc(t.status ?? "Not recorded")}</code><br>Field review: <code>${esc(t.response_review?.status ?? "Not recorded")}</code></p></td>` +
        `<td><p>${esc(run.verdict)}</p>${link}</td></tr>`;
    }).join("");
    return `<p>Follow the development sequence. Expand a setup to inspect recorded assistance and budgets, then open the original attempt.</p>` +
      `<p class="boundary">Task wording, host assistance and budgets changed across these attempts. This is not a controlled benchmark. Completed tool work, a returned response and faithful explanation are separate outcomes. Review findings are AI-assisted, not independent human evaluation.</p>` +
      `<p class="morning-scroll-hint">On a narrow screen, scroll the table sideways to reach the review and recording links.</p>` +
      `<div class="morning-table-scroll" role="region" aria-label="Morning-review attempt comparison" tabindex="0"><table><caption>Morning-review development sequence · ${morning.length} recordings</caption><thead><tr><th scope="col">Attempt and setup</th><th scope="col">Recorded result</th><th scope="col">Review finding · AI-assisted</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  }
  const api = { render, renderComparisons, renderMorningComparison, renderCorrectionComparison };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CSM_MODEL_TURNS = api;
})(typeof window !== "undefined" ? window : this);
