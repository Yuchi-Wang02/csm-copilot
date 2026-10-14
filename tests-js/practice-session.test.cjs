const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");
const core = require("../demo/practice-core.js");
const files = require("../demo/practice-session.js");
const context = { window: {} };
vm.createContext(context);
for (const name of ["data.js", "model-runs.js"])
  vm.runInContext(fs.readFileSync(path.join(__dirname, "../demo", name), "utf8"), context);
const cases = JSON.parse(JSON.stringify(core.buildCases(context.window.CSM_DATA, context.window.CSM_MODEL_RUNS)));
const asOf = context.window.CSM_DATA.workflow.as_of;
const clone = (x) => JSON.parse(JSON.stringify(x));
function mixedSession() {
  const session = core.createSession(cases);
  session[0].choice = "approve";
  session[0].reasoning = "QA only: first reasoning. 未经审核。";
  session[0] = core.reveal(session[0], cases[0]);
  session[0].reflection = "QA only: later reflection. <script>doNotRun()</script>";
  session[3].reasoning = "QA only: unfinished note without an option.";
  session[4].choice = "clarify_invoice";
  return session;
}
test("a mixed session round-trips first responses, reflection, drafts and selection", async () => {
  const session = mixedSession(), before = clone(session);
  const saved = await files.save(cases, session, "callback_handoff", asOf);
  const loaded = await files.load(saved, cases, asOf);
  assert.deepEqual(loaded, {session, selectedId:"callback_handoff"});
  assert.deepEqual(session, before);
  loaded.session[0].reflection = "Caller edit";
  assert.deepEqual(session, before);
  assert.equal(JSON.parse(saved).items[3].reviewed, false);
  assert.doesNotMatch(saved, /exercise guidance|qwen4-constrained.json|expected|explanation/);
});
test("stable case and option IDs survive catalog and file reordering", async () => {
  const session = mixedSession();
  const saved = JSON.parse(await files.save(cases, session, cases[0].id, asOf));
  saved.items.reverse();
  const reordered = clone(cases).reverse();
  reordered.forEach((c) => c.options.reverse());
  const loaded = await files.load(JSON.stringify(saved), reordered, asOf);
  assert.deepEqual(loaded.session, [...session].reverse());
  assert.equal(loaded.selectedId, cases[0].id);
});
test("changed evidence, policy, prompt or snapshot requires keeping the old file separately", async () => {
  const saved = await files.save(cases, mixedSession(), cases[0].id, asOf);
  for (const change of [
    (c) => { c[0].evidence[0].value = "new evidence"; },
    (c) => { c[0].expected = "approve"; },
    (c) => { c[0].options[0].feedback = "changed guidance"; },
    (c) => { c[0].prompt = "changed task"; },
  ]) {
    const altered = clone(cases); change(altered);
    await assert.rejects(files.load(saved, altered, asOf), /different exercise content/);
  }
  await assert.rejects(files.load(saved, cases, "later snapshot"), /different exercise content/);
});
test("invalid inputs never return a replacement session", async () => {
  const session = mixedSession(), before = clone(session);
  const saved = JSON.parse(await files.save(cases, session, cases[0].id, asOf));
  for (const change of [
    (f) => { f.items.pop(); },
    (f) => { f.items[1] = clone(f.items[0]); },
    (f) => { f.items[0].id = "not_a_case"; },
    (f) => { f.items[0].choice = "not_an_option"; },
    (f) => { f.items[0].reviewed = "true"; },
    (f) => { f.items[0].initial.reasoning = "Rewritten first answer"; },
    (f) => { f.items[3].reflection = "Not yet reviewed"; },
    (f) => { f.items[3].initial = {}; },
    (f) => { f.items[0].reasoning = "x".repeat(4001); },
    (f) => { f.items[3].reasoning = {html:"<b>not text</b>"}; },
    (f) => { f.selected_id = "missing"; },
    (f) => { f.format = "future-format"; },
    (f) => { f.source = "https://example.com/untrusted"; },
    (f) => { f.items[0].__proto__ = {injected:true}; f.items[0].unexpected = true; },
  ]) {
    const altered = clone(saved); change(altered);
    await assert.rejects(files.load(JSON.stringify(altered), cases, asOf));
    assert.deepEqual(session, before);
  }
  for (const content of ["# readable notes", "null", "[]", "x".repeat(files.MAX_BYTES + 1)])
    await assert.rejects(files.load(content, cases, asOf));
});
test("4000-character Unicode notes fit the byte limit and remain literal in readable exports", async () => {
  const session = core.createSession(cases);
  session[0].reasoning = "中".repeat(4000);
  session[1].reasoning = '<script>doNotRun()</script>\n# Fake section\n[go](javascript:run())';
  const saved = await files.save(cases, session, cases[1].id, asOf);
  const loaded = await files.load(saved, cases, asOf);
  assert.equal(loaded.session[0].reasoning.length, 4000);
  const md = core.exportReflection(cases, loaded.session, asOf, true);
  assert.match(md, /resumed from a user-editable local progress file/);
  assert.match(md, /do not verify authorship, timing or unaided work/);
  assert.doesNotMatch(md, /<script>|\n# Fake section|\[go\]\(javascript:/);
  assert.equal(loaded.session[1].reviewed, false);
});
test("save captures state before its asynchronous content check completes", async () => {
  const session = mixedSession();
  const saving = files.save(cases, session, cases[0].id, asOf);
  session[0].reflection = "A later edit";
  const loaded = await files.load(await saving, cases, asOf);
  assert.notEqual(loaded.session[0].reflection, session[0].reflection);
});
