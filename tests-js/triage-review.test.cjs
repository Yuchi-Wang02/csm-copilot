const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");
const api = require("../demo/triage-review.js");
const root = path.join(__dirname, "..");
const report = JSON.parse(fs.readFileSync(path.join(root, "evidence/callback-denial-review.json"), "utf8"));
const row = (id) => report.cases.find((c) => c.id === id);

test("browser replay matches the published sixteen-case report exactly", () => {
  const context = {window:{}}; vm.createContext(context);
  vm.runInContext(fs.readFileSync(path.join(root, "demo/data.js"), "utf8"), context);
  assert.equal(JSON.stringify(context.window.CSM_DATA.callback_denial), JSON.stringify(report));
  assert.equal(report.cases.length, 16);
  assert.equal(report.changed_cases.length, 7);
  assert.equal(report.remaining_mismatches.length, 3);
});

test("a repaired denial shows both categories and the clarification route without diagnosing", () => {
  const probe = row("callback_denial_en"), before = JSON.stringify(probe);
  const html = api.render(probe);
  assert.match(html, /Before repair<\/h4><p>reward callback/);
  assert.match(html, /Current categories<\/h4><p>unknown/);
  assert.match(html, /Changed; matches project expectation/);
  assert.match(html, /clarify scope/);
  assert.match(html, /Root cause:<\/strong> unconfirmed/);
  assert.match(html, /Explicitly denied callback/);
  assert.equal(JSON.stringify(probe), before);
});

test("known failures remain mismatches and separate positive symptoms remain visible", () => {
  const failure = api.render(row("not_failing"));
  assert.match(failure, /Still differs from project expectation/);
  assert.match(failure, /Current categories<\/h4><p>reward callback/);
  assert.match(failure, /Project expectation<\/h4><p>unknown/);
  const positive = api.render(row("separate_callback"));
  assert.match(positive, /Unchanged; matches project expectation/);
  assert.match(positive, /Current categories<\/h4><p>reward callback/);
  assert.match(api.render(row("denied_with_blank_zh")), /Current categories<\/h4><p>no offers/);
});

test("probe text and tool output cannot introduce active markup", () => {
  const probe = JSON.parse(JSON.stringify(row("callback_denial_en")));
  probe.text = '<img src=x onerror="run()">';
  probe.after_result.notes = ['<script>run()</script>'];
  probe.after_result.route = '<iframe>';
  const html = api.render(probe);
  assert.doesNotMatch(html, /<img|<script|<iframe/);
  assert.match(html, /&lt;img/);
  assert.match(html, /&lt;script/);
  assert.match(html, /&lt;iframe/);
});
