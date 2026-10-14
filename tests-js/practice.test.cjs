const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");
const api = require("../demo/practice-core.js");
const root = path.join(__dirname, "..");
const context = { window: {} };
vm.createContext(context);
for (const file of ["data.js", "model-runs.js"])
  vm.runInContext(
    fs.readFileSync(path.join(root, "demo", file), "utf8"),
    context,
  );
const cases = api.buildCases(
  context.window.CSM_DATA,
  context.window.CSM_MODEL_RUNS,
);

test("notes can be saved before any guidance is revealed", () => {
  const session = api.createSession(cases);
  assert.equal(api.hasWork(session), false);
  session[0].reasoning = "   ";
  assert.equal(api.hasWork(session), false);
  session[0].reasoning = "My first hypothesis";
  assert.equal(api.hasWork(session), true);
  session[0].reasoning = "";
  session[1].choice = "review";
  assert.equal(api.hasWork(session), true);
});

test("unfinished choices and notes survive export without implying review", () => {
  const session = api.createSession(cases);
  session[0].choice = "approve";
  session[1].reasoning = "我的初步想法\n# My heading\n<script>test</script>";
  const before = JSON.stringify(session);
  const out = api.exportReflection(cases, session, "2026-10-14");
  assert.match(out, /Confirm Friday/);
  assert.match(out, /我的初步想法/);
  assert.match(out, /Draft choice \(not compared with guidance\)/);
  assert.match(out, /Draft reasoning \(guidance not revealed\)/);
  assert.ok(!out.includes("\n# My heading"));
  assert.ok(!out.includes("<script>"));
  assert.ok(!out.includes("Project guidance:"));
  assert.ok(!out.includes("Option comparison:"));
  assert.equal((out.match(/Status: not reviewed/g) || []).length, cases.length);
  assert.equal(JSON.stringify(session), before);
});

test("AI practice evidence opens the specific recording used by the exercise", () => {
  const source = new URL(cases[2].source, "https://yuchi-wang02.github.io/csm-copilot/");
  assert.equal(source.searchParams.get("run"), "qwen4-constrained");
  assert.equal(source.hash, "#model-runs");
});
test("practice decisions remain supported by the published evidence", () => {
  const states = Object.fromEntries(
    cases[0].evidence.map((e) => [e.label, e.value]),
  );
  assert.equal(states["Non-test device verification"], "not_met");
  assert.equal(states["Reward callback verification"], "unknown");
  assert.equal(states["Platform currency approval"], "met");
  assert.equal(states["Production visibility setting"], "met");
  assert.ok(cases[1].evidence.every((e) => e.value === "met"));
  const ios = context.window.CSM_DATA.workflow.packets
    .flatMap((p) => p.integrations)
    .find((i) => i.readiness.integration_id === "lantern_ios");
  assert.equal(ios.followup_en.intent, "launch_plan_review");
  assert.equal(cases[2].evidence[0].value, "structured_fields_match");
  assert.equal(cases[2].evidence[1].value, "not_performed");
  assert.equal(cases[2].evidence[2].value, "2");
});
test("reveal requires a valid option and preserves the initial response", () => {
  const item = api.createSession(cases)[0];
  assert.equal(api.reveal(item, cases[0]), item);
  item.choice = "invented";
  assert.equal(api.reveal(item, cases[0]), item);
  item.choice = "approve";
  item.reasoning = "My original explanation";
  const reviewed = api.reveal(item, cases[0]);
  item.reasoning = "changed";
  assert.equal(reviewed.initial.reasoning, "My original explanation");
  assert.equal(reviewed.initial.choice, "approve");
  assert.equal(api.reveal(reviewed, cases[0]), reviewed);
});
test("export distinguishes initial work, later reflection and unreviewed decisions", () => {
  const session = api.createSession(cases);
  session[0].choice = "retest";
  session[0].reasoning = "Retest the failed device.";
  session[0] = api.reveal(session[0], cases[0]);
  session[0].reflection = "I also need callback evidence.";
  session[1].reasoning = "An unfinished second decision";
  const out = api.exportReflection(cases, session, "2026-10-14");
  assert.match(out, /Reasoning captured before guidance/);
  assert.match(out, /Reflection written after guidance/);
  assert.equal((out.match(/Status: not reviewed/g) || []).length, cases.length - 1);
  assert.match(out, /Written reasoning remains ungraded/);
  assert.match(out, /lantern_android_device_verified/);
  assert.match(out, /An unfinished second decision/);
  assert.equal(session[1].reviewed, false);
});
test("user notes cannot inject HTML, headings or active Markdown links into the report", () => {
  const session = api.createSession(cases);
  session[0].choice = "retest";
  session[0].reasoning =
    "<script>alert(1)</script>\n# Certified\n[click](https://example.com)";
  session[0] = api.reveal(session[0], cases[0]);
  const out = api.exportReflection(cases, session, "snapshot");
  assert.ok(!out.includes("<script>"));
  assert.ok(!out.includes("\n# Certified"));
  assert.ok(!out.includes("[click](https://example.com)"));
  assert.ok(out.includes("&lt;script&gt;"));
});
test("reset creates a clean independent session without claiming mastery", () => {
  const session = api.createSession(cases);
  session[0].reasoning = "old";
  session[0].choice = "retest";
  session[0] = api.reveal(session[0], cases[0]);
  const fresh = api.createSession(cases);
  assert.ok(
    fresh.every((s) => !s.reviewed && s.reasoning === "" && s.initial === null),
  );
  assert.equal(session[0].initial.reasoning, "old");
  assert.match(
    api.exportReflection(cases, fresh, "snapshot"),
    /not an assessment or verified personal mastery/,
  );
});

test("callback practice is grounded in the original report and scoped handoff gaps", () => {
  const decision = cases.find((c) => c.id === "callback_handoff");
  const packet = context.window.CSM_DATA.workflow.packets.find((p) => p.context.account.id === "acc_006");
  const source = packet.context.evidence.find((e) => e.id === "msg_issue_callback");
  const ticket = packet.tickets.find((t) => t.draft_id === "ticket-issue_callback");
  assert.equal(decision.evidence[0].value, source.text);
  assert.match(source.text, /self-managed.*HTTP 405/);
  assert.equal(decision.evidence[1].value, `${source.kind} · ${source.at}`);
  for (const value of [ticket.fields.sdk_version, ticket.fields.region, ticket.fields.time_window]) assert.ok(decision.evidence[2].value.includes(value));
  assert.equal(decision.evidence[3].value, ticket.missing_fields.join(", "));
  assert.equal(decision.evidence[3].value, "reproduction_steps, redacted_logs");
  assert.equal(decision.evidence[4].value, "unconfirmed");
  assert.equal(decision.expected, "collect_missing");
  assert.equal(new Set(cases.map((c) => c.id)).size, 4);
  assert.equal(decision.source, "?case=harbor_android&view=handoff&lang=en#workspace");
});

test("fourth decision preserves first reasoning, later reflection and its evidence in the download", () => {
  const session = api.createSession(cases), index = cases.findIndex((c) => c.id === "callback_handoff");
  session[index].choice = "repeat_all";
  session[index].reasoning = "QA-only initial reasoning, not Yuchi's work.";
  session[index] = api.reveal(session[index], cases[index]);
  session[index].reflection = "QA-only later reflection.";
  const out = api.exportReflection(cases, session, "2026-10-14");
  assert.equal(session[index].initial.choice, "repeat_all");
  assert.match(out, /QA\\-only initial reasoning/);
  assert.match(out, /QA\\-only later reflection/);
  assert.match(out, /Option comparison: differs from the project policy/);
  assert.match(out, /msg_issue_callback/);
  assert.match(out, /case=harbor_android&view=handoff&lang=en#workspace/);
  assert.equal((out.match(/Status: not reviewed/g) || []).length, 3);
});
