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
  const out = api.exportReflection(cases, session, "2026-10-14");
  assert.match(out, /Reasoning captured before guidance/);
  assert.match(out, /Reflection written after guidance/);
  assert.equal((out.match(/Status: not reviewed/g) || []).length, 2);
  assert.match(out, /Written reasoning remains ungraded/);
  assert.match(out, /lantern_android_device_verified/);
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
