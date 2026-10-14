const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const api = require("../demo/model-turns.js");
const directory = path.join(__dirname, "../evidence/model-runs");
const trace = (id) => JSON.parse(fs.readFileSync(path.join(directory, id + ".json"), "utf8"));

test("every recording retains its model turns, initial messages and raw audit view without mutation", () => {
  const names = fs.readdirSync(directory).filter((n) => n !== "review.json" && n.endsWith(".json"));
  assert.equal(names.length, 10);
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
  for (const id of ["qwen06-single", "qwen4-single"]) {
    const html = api.render(trace(id));
    assert.match(html, /Host rejected the proposed action/);
    assert.match(html, /No tool calls were executed in this turn/);
    assert.doesNotMatch(html, /<h4>Tool execution through MCP<\/h4>/);
    assert.doesNotMatch(html, /4 recorded tool calls/);
  }
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
