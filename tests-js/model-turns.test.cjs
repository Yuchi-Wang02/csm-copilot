const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const api = require("../demo/model-turns.js");
const directory = path.join(__dirname, "../evidence/model-runs");
const trace = (id) => JSON.parse(fs.readFileSync(path.join(directory, id + ".json"), "utf8"));

test("correction comparison displays the actual removed citation and unchanged explanation once", () => {
  const data = JSON.parse(fs.readFileSync(path.join(__dirname, "../demo/model-runs.js"), "utf8").replace(/^window.CSM_MODEL_RUNS = /, "").replace(/;\s*$/, ""));
  const comparison = data.runs.find(r => r.id === "qwen4-morning-correction").correction_comparison;
  const before = JSON.stringify(comparison), html = api.renderCorrectionComparison(comparison);
  assert.match(html, /What changed after the correction/);
  assert.equal((html.match(/Removed in correction/g) || []).length, 1);
  assert.equal((html.match(/UNCHANGED IN BOTH ANSWERS/g) || []).length, 2);
  assert.equal(html.split(comparison.rows[2].before).length - 1, 1);
  assert.match(html, /steps\[7\].actions\[0\].final.platforms\[0\].evidence_ids/);
  assert.match(html, /steps\[8\].actions\[0\].final.handoffs\[0\].evidence_ids/);
  assert.match(html, /expected values/);
  assert.equal(JSON.stringify(comparison), before);
});

test("correction comparison escapes saved values, feedback and source paths", () => {
  assert.equal(api.renderCorrectionComparison(null), "");
  const html = api.renderCorrectionComparison({
    before_turn: 8, after_turn: 9,
    rows: [{label: "<script>", before: ['<img src=x>'], after: [], paths: ['<svg>']}],
    feedback: {content: '<iframe>'}, feedback_path: '<source>', boundary: '<object>',
  });
  assert.match(html, /&lt;img src=x&gt;/);
  assert.match(html, /&lt;iframe&gt;/);
  assert.match(html, /&lt;svg&gt;/);
  assert.doesNotMatch(html, /<script>|<img|<iframe|<svg|<object>/);
});

test("morning correction keeps the rejected answer, supplied feedback and unverified prose distinct", () => {
  const input = trace("qwen4-morning-correction"), before = JSON.stringify(input);
  const html = api.render(input);
  assert.match(html, /Turn 8 — Host rejected the structured response/);
  assert.match(html, /Turn 9 — Structured fields matched; prose still needs review/);
  assert.equal((html.match(/<h4>Host correction request 1<\/h4>/g) || []).length, 1);
  assert.match(html, /It may include expected values; this is assisted recovery/);
  assert.match(html, /retained 21 of 29 messages/);
  assert.equal(input.steps[7].actions[0].final.explanation, input.final.explanation);
  assert.equal(input.steps[8].tool_calls, undefined);
  assert.equal(JSON.stringify(input), before);
});

test("morning comparison separates recorded coverage, missing finals and field rejection", () => {
  const review = JSON.parse(fs.readFileSync(path.join(directory, "review.json"), "utf8"));
  const runs = review.runs.map((entry) => ({...entry, trace: trace(entry.id)}));
  const before = JSON.stringify(runs), html = api.renderMorningComparison(runs);
  assert.equal((html.match(/<th scope="row">/g) || []).length, 8);
  assert.equal((html.match(/0 \/ 7 requested actions observed/g) || []).length, 3);
  assert.equal((html.match(/7 \/ 7 requested actions observed/g) || []).length, 5);
  assert.equal((html.match(/No final response recorded/g) || []).length, 4);
  assert.equal((html.match(/<p>Final response recorded<\/p>/g) || []).length, 4);
  assert.equal((html.match(/Field review: <code>rejected/g) || []).length, 2);
  assert.match(html, /Host status: <code>host_error/);
  assert.match(html, /Response wait budget<\/dt><dd>Not recorded/);
  assert.match(html, /Response wait budget<\/dt><dd>600 seconds/);
  assert.match(html, /Output-token cap<\/dt><dd>1536/);
  assert.match(html, /Correction budget<\/dt><dd>0/);
  assert.match(html, /Review finding · AI-assisted/);
  assert.match(html, /not a controlled benchmark/);
  assert.match(html, /\?run=qwen4-morning-compact-context#model-result/);
  assert.doesNotMatch(html, /\?run=qwen4-batch/);
  assert.equal(JSON.stringify(runs), before);
});

test("comparison preserves unknown settings, escapes data and withholds ambiguous recording links", () => {
  assert.equal(api.renderMorningComparison([]), "");
  const entry = {id: "qa", label: '<img src=x>', verdict: '<script>review</script>',
    trace: {task_id: "morning_review", enforce_dependencies: false, repair_budget: 0,
      status: '<iframe>', coverage: {observed: 0, required: 7}}};
  const runs = [entry], before = JSON.stringify(runs);
  const html = api.renderMorningComparison(runs);
  assert.match(html, /Dependency policy<\/dt><dd>Disabled/);
  assert.match(html, /Constrained actions<\/dt><dd>Not recorded/);
  assert.match(html, /Final-response presence not recorded/);
  assert.match(html, /&lt;img src=x&gt;/);
  assert.match(html, /&lt;script&gt;review/);
  assert.doesNotMatch(html, /<img|<script|<iframe/);
  assert.equal(JSON.stringify(runs), before);
  assert.doesNotMatch(api.renderMorningComparison([entry, structuredClone(entry)]), /data-review-link/);
  assert.match(api.renderMorningComparison([{...entry, id: 'qa" onclick="bad'}]), /Recording link unavailable/);
});

test("optional context reduction exposes omissions without claiming inference improvement", () => {
  const input = trace("qwen4-morning-field-review");
  input.steps[7].context_reduction = {
    original_message_count: 25, retained_message_count: 18,
    boundary: "Authored software test: no speed or quality claim. <script>",
    omitted_messages: [{original_index: 2, message: {role: "user", content: "<img src=x>"}}],
  };
  const before = JSON.stringify(input), html = api.render(input);
  assert.match(html, /Final context reduction/);
  assert.match(html, /retained 18 of 25 messages/);
  assert.match(html, /Inspect omitted host messages and original positions/);
  assert.match(html, /steps\[7\].context_reduction/);
  assert.match(html, /no speed or quality claim/);
  assert.match(html, /&lt;img|&lt;script/);
  assert.doesNotMatch(html, /<img|<script/);
  assert.equal(JSON.stringify(input), before);
  assert.doesNotMatch(api.render(trace("qwen4-morning-field-review")), /Final context reduction/);
});

test("an optional final contract remains visible as host assistance and inert text", () => {
  const input = trace("qwen4-morning-long-budget"), step = input.steps[7];
  step.final_contract_message = {role: "system", content: "<img src=x> Require separate unknown and failed fields."};
  step.actions = [{final: {explanation: "Authored test explanation"}}];
  step.response_review = {status: "rejected", free_text_verification: "not_performed", boundary: "Test field mismatch"};
  const before = JSON.stringify(input), html = api.render(input);
  assert.match(html, /Host final-answer contract/);
  assert.match(html, /instructions are assistance, not model-written reasoning/);
  assert.match(html, /steps\[7\].final_contract_message/);
  assert.match(html, /&lt;img src=x&gt;/);
  assert.doesNotMatch(html, /<img/);
  assert.match(html, /Turn 8 — Host rejected the structured response/);
  assert.ok(html.indexOf("Host final-answer contract") < html.lastIndexOf("<h4>Model proposal"));
  assert.equal(JSON.stringify(input), before);
});

test("the actual morning field-review recording exposes its rejected citation and host contract", () => {
  const input = trace("qwen4-morning-field-review"), before = JSON.stringify(input);
  const html = api.render(input);
  assert.match(html, /Turn 8 — Host rejected the structured response/);
  assert.match(html, /Host final-answer contract/);
  assert.match(html, /steps\[7\].final_contract_message/);
  assert.match(html, /The model worker reported schema-constrained generation for this turn/);
  assert.match(html, /lantern_android.evidence_ids/);
  assert.match(html, /msg_issue_blank/);
  assert.match(html, /device verification failed/);
  assert.match(html, /Free-text verification: <code>not_performed/);
  assert.doesNotMatch(html, /Host correction request|Structured fields matched; prose still needs review/);
  assert.equal(JSON.stringify(input), before);
});

test("the actual compact-context run exposes its omission audit and unchanged citation failure", () => {
  const input = trace("qwen4-morning-compact-context"), before = JSON.stringify(input);
  const html = api.render(input);
  assert.match(html, /Final context reduction/);
  assert.match(html, /retained 18 of 25 messages/);
  assert.match(html, /steps\[7\].context_reduction/);
  assert.match(html, /Inspect omitted host messages and original positions/);
  assert.match(html, /Turn 8 — Host rejected the structured response/);
  assert.match(html, /lantern_android.evidence_ids/);
  assert.match(html, /msg_issue_blank/);
  assert.doesNotMatch(html, /Host correction request|Structured fields matched; prose still needs review/);
  assert.equal(JSON.stringify(input), before);
});

test("a saved request without a response is not displayed as a model proposal", () => {
  for (const state of ["prepared", "sent", "response_timeout", "response_error", "cancelled", "host_error"]) {
    const input = {status: state, error_type: "TimeoutError", error_causes: [{type: "TimeoutError", message: "<script>"}], steps: [{
      number: 8, request_state: state, response_timeout_seconds: 180,
      worker_request: {messages: [{role: "user", content: "<img src=x>"}], json_schema: {type: "object"}},
      request_sha256: "test-hash", request_encoding: "UTF-8 JSON followed by LF",
      response_error: {type: "TimeoutError", message: "<script>", partial_output_captured: false},
      failure_phase: "dispatch", worker_response_text: "<script>invalid JSON",
    }]};
    const before = JSON.stringify(input), html = api.render(input);
    assert.match(html, /Recorded worker request/);
    assert.match(html, /No model response recorded/);
    assert.match(html, /Response budget: 180 seconds/);
    assert.match(html, /not acknowledged by the model/);
    assert.match(html, /does not establish whether the worker received any bytes/);
    assert.match(html, /Inspect the invalid worker envelope/);
    assert.match(html, /Inspect recorded failure causes/);
    assert.doesNotMatch(html, /<h4>Model proposal|Read the unedited model output|<img|<script>/);
    assert.equal(JSON.stringify(input), before);
  }
});

test("claim comparison keeps quoted source fields and review separate and escaped", () => {
  const rows = [{claim: '<img src=x>', assessment: 'Authored review <script>', source_label: 'Turn 1 · call 2',
    fields: [{label: 'Decision', path: 'steps[0].tool_calls[1].tool_result.decision', value: 'checklist_complete'},
      {label: 'Evidence', path: 'raw <path>', value: ['record_1', '<img>']}]}];
  const before = JSON.stringify(rows);
  const html = api.renderComparisons(rows);
  assert.match(html, /MODEL EXCERPT · UNVERIFIED/);
  assert.match(html, /RECORDED TOOL FIELDS/);
  assert.match(html, /checklist_complete/);
  assert.match(html, /steps\[0\].tool_calls\[1\].tool_result.decision/);
  assert.match(html, /not an automated semantic verdict/);
  assert.match(html, /&lt;img/);
  assert.doesNotMatch(html, /<img|<script/);
  assert.equal(JSON.stringify(rows), before);
  assert.equal(api.renderComparisons([]), '');
  assert.equal(api.renderComparisons(undefined), '');
});

test("every recording retains its model turns, initial messages and raw audit view without mutation", () => {
  const names = fs.readdirSync(directory).filter((n) => n !== "review.json" && n.endsWith(".json"));
  assert.equal(names.length, 18);
  for (const name of names) {
    const input = trace(name.slice(0, -5)), before = JSON.stringify(input);
    const html = api.render(input);
    assert.equal((html.match(/class="model-turn"/g) || []).length, input.steps.length, name);
    assert.equal((html.match(/<h4>Recorded .* message<\/h4>/g) || []).length, input.initial_messages.length, name);
    assert.match(html, /Inspect raw model turns and tool results/);
    assert.match(html, /performs no inference or tool calls/);
    assert.equal(JSON.stringify(input), before, name);
  }
});
test("successful tool calls and an unsupported final statement stay distinct", () => {
  const html = api.render(trace("qwen4-batch"));
  assert.match(html, /Turn 1 — 4 recorded tool calls · results received/);
  assert.match(html, /Turn 2 — Model supplied a final response; prose unverified/);
  assert.match(html, /full compliance/);
  assert.match(html, /No evidence IDs are missing for Android/);
  assert.match(html, /lantern_android_device_verified/);
  assert.match(html, /checklist_complete/);
  assert.match(html, /current tools may differ/);
  assert.doesNotMatch(html, /Structured fields matched|Host correction request/);
});
test("parser rejection does not turn proposed tool names into executed calls", () => {
  for (const id of ["qwen06-single", "qwen4-single", "qwen4-morning-review", "qwen4-morning-sequenced", "qwen4-morning-enforced"]) {
    const html = api.render(trace(id));
    assert.match(html, /Host rejected the proposed action/);
    assert.match(html, /No tool calls were executed in this turn/);
    assert.doesNotMatch(html, /<h4>Tool execution through MCP<\/h4>/);
    assert.doesNotMatch(html, /4 recorded tool calls/);
  }
});

test("host policy input is visible before the model proposal without claiming policy rejection", () => {
  const input = trace("qwen4-morning-enforced"), before = JSON.stringify(input);
  const html = api.render(input);
  assert.match(html, /Host state supplied before this proposal/);
  assert.match(html, /pending actions as planning assistance/);
  assert.match(html, /Stage: <code>awaiting_queue<\/code> · 1 pending action · Final response not allowed/);
  assert.match(html, /steps\[0\].policy_message/);
  assert.match(html, /Read the exact host state message/);
  assert.ok(html.indexOf("Host state supplied") < html.indexOf("<h4>Model proposal"));
  assert.match(html, /An action batch must contain 1..4 actions/);
  assert.doesNotMatch(html, /Host dependency validation|Host rejected the dependency proposal/);
  assert.equal(JSON.stringify(input), before);
});

test("dependency rejection and result failure retain their distinct stopping boundaries", () => {
  const input = trace("qwen4-morning-enforced");
  delete input.steps[0].parse_error;
  input.steps[0].policy_error = "Requested work remains";
  let html = api.render(input);
  assert.match(html, /Host rejected the dependency proposal/);
  assert.match(html, /whole proposal was rejected before tool execution/);
  delete input.steps[0].policy_error;
  input.steps[0].tool_calls = [{action: {tool: "check_readiness", arguments: {integration_id: "a"}},
    tool_error: false, tool_result: {integration_id: "b"}, policy_result_error: "Wrong scope"}];
  html = api.render(input);
  assert.match(html, /Host stopped after a result failed dependency checks/);
  assert.match(html, /Later actions in this batch were not executed/);
  assert.doesNotMatch(html, /No tool calls were executed in this turn/);
  delete input.steps[0].tool_calls[0].policy_result_error;
  input.steps[0].tool_calls[0].policy_after = {stage: "reviewing", pending_actions: []};
  html = api.render(input);
  assert.match(html, /Host dependency state after this result/);
});

test("policy messages, state and result errors are escaped as data", () => {
  const input = trace("qwen4-morning-enforced");
  const payload = '<img src=x onerror="run()">';
  input.steps[0].policy_message.content = payload;
  input.steps[0].policy_before.stage = payload;
  input.steps[0].policy_error = payload;
  input.steps[0].tool_calls = [{action: {tool: "check_readiness", arguments: {}}, tool_result: {},
    policy_result_error: payload, policy_after: {stage: payload}}];
  const html = api.render(input);
  assert.doesNotMatch(html, /<img|<script/);
  assert.ok((html.match(/&lt;img/g) || []).length >= 5);
});
test("a failed call remains visible beside other calls that received results", () => {
  const html = api.render(trace("qwen4-callback-input-guard"));
  assert.match(html, /4 recorded tool calls · 1 tool error/);
  assert.match(html, /Recorded error response/);
  assert.match(html, /draft_ticket/);
  assert.match(html, /ticket-issue_callback/);
  assert.doesNotMatch(html, /No tool calls were executed in this turn/);
});
test("host corrections and field matching are tied to their actual turns without certifying prose", () => {
  const html = api.render(trace("qwen4-constrained"));
  assert.match(html, /Turn 2 — Host rejected the structured response/);
  assert.match(html, /Turn 3 — Host rejected the structured response/);
  assert.match(html, /Turn 4 — Structured fields matched; prose still needs review/);
  assert.equal((html.match(/<h4>Host correction request /g) || []).length, 2);
  assert.match(html, /this is assisted recovery/);
  assert.match(html, /Free-text verification: <code>not_performed<\/code>/);
  assert.match(html, /msg_issue_blank/);
});

test("generation constraints are visible as host assistance rather than factual verification", () => {
  const input = trace("qwen4-constrained"), before = JSON.stringify(input);
  const html = api.render(input);
  const constrained = input.steps.filter((step) => step.generation_schema);
  assert.ok(constrained.length > 0);
  assert.equal((html.match(/<h4>Host requested constrained generation<\/h4>/g) || []).length, constrained.length);
  assert.match(html, /decoding assistance; it does not verify factual claims/);
  assert.match(html, /model worker reported schema-constrained generation/);
  assert.match(html, /Inspect the generation schema/);
  assert.equal(JSON.stringify(input), before);
  assert.doesNotMatch(api.render(trace("qwen4-morning-enforced")), /Host requested constrained generation/);
  input.steps[0].generation_schema = {description: '<script>untrusted</script>'};
  input.steps[0].model_response.schema_constrained = false;
  const altered = api.render(input);
  assert.match(altered, /does not confirm that the decoding constraint was active/);
  assert.match(altered, /&lt;script&gt;/);
  assert.doesNotMatch(altered, /<script>/);
});

test("a constrained workflow ending in a host error keeps seven calls separate from a missing final", () => {
  const input = trace("qwen4-morning-constrained"), before = JSON.stringify(input);
  const html = api.render(input);
  assert.equal((html.match(/1 recorded tool call · results received/g) || []).length, 7);
  assert.equal((html.match(/<h4>Host requested constrained generation<\/h4>/g) || []).length, 7);
  assert.match(html, /Recorded terminal status: <code>host_error/);
  assert.match(html, /Recorded host error type: <code>ExceptionGroup/);
  assert.match(html, /ticket-issue_blank/);
  assert.doesNotMatch(html, /Model supplied a final response|Model-written explanation from the parsed final response/);
  assert.equal(JSON.stringify(input), before);
  input.error_type = '<img src=x>';
  assert.doesNotMatch(api.render(input), /<img/);
});

test("the longer-budget recording exposes eight exact requests and its unedited final answer", () => {
  const input = trace("qwen4-morning-long-budget"), before = JSON.stringify(input);
  const html = api.render(input);
  assert.equal((html.match(/<h4>Recorded worker request<\/h4>/g) || []).length, 8);
  assert.equal((html.match(/1 recorded tool call · results received/g) || []).length, 7);
  assert.match(html, /Turn 8 — Model supplied a final response; prose unverified/);
  assert.match(html, /Response budget: 600 seconds/);
  assert.match(html, /missing currency approval and device verification/);
  assert.match(html, /not_met/);
  assert.doesNotMatch(html, /No model response recorded|Worker response timed out|Recorded host error type/);
  assert.equal(JSON.stringify(input), before);
});
test("exhausted parse corrections do not imply a later accepted answer", () => {
  const html = api.render(trace("qwen4-grounded-corrections"));
  assert.equal((html.match(/No tool calls were executed in this turn/g) || []).length, 3);
  assert.equal((html.match(/<h4>Host correction request /g) || []).length, 2);
  assert.match(html, /Recorded terminal status: <code>invalid_action/);
  assert.doesNotMatch(html, /Structured fields matched|Model supplied a final response/);
});
test("model text, arguments, errors, host feedback and message roles remain inert text", () => {
  const input = trace("qwen4-constrained");
  const payload = '<img src=x onerror="run()">';
  input.initial_messages[0].role = payload;
  input.initial_messages[0].content = payload;
  input.steps[0].model_response.text = payload;
  input.steps[0].tool_calls[0].action.tool = payload;
  input.steps[0].tool_calls[0].action.arguments.integration_id = payload;
  input.steps[0].tool_calls[0].tool_result.boundary = payload;
  input.steps[1].correction_feedback.content = payload;
  input.steps[1].response_review.boundary = payload;
  input.steps[2].parse_error = payload;
  const html = api.render(input);
  assert.doesNotMatch(html, /<img|<script/);
  assert.ok((html.match(/&lt;img/g) || []).length >= 9);
});
