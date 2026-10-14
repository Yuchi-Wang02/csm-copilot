const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const path = require("node:path");
const api = require("../demo/review-links.js");
const context = { window: {} };
vm.createContext(context);
vm.runInContext(
  fs.readFileSync(path.join(__dirname, "../demo/data.js"), "utf8"),
  context,
);
const workflow = context.window.CSM_DATA.workflow;
vm.runInContext(
  fs.readFileSync(path.join(__dirname, "../demo/model-runs.js"), "utf8"),
  context,
);
const runs = context.window.CSM_MODEL_RUNS.runs;

test("each published recording has a stable direct link independent of the latest attempt", () => {
  for (const run of runs) {
    const link = new URL(api.shareRun(run.id, runs));
    assert.equal(link.origin, "https://yuchi-wang02.github.io");
    assert.equal(link.pathname, "/csm-copilot/");
    assert.equal(link.hash, "#model-runs");
    assert.deepEqual([...link.searchParams.keys()], ["run"]);
    assert.deepEqual(api.readRun(link.search, runs), {runId:run.id, invalid:false});
    assert.equal(api.readRun(link.search, [...runs, {id:"future-attempt"}]).runId, run.id);
  }
});
test("unknown, empty or duplicated recording IDs fall back visibly; an absent ID is normal", () => {
  assert.deepEqual(api.readRun("", runs), {runId:runs.at(-1).id, invalid:false});
  for (const search of ["?run=", "?run=missing", "?run=%3Cscript%3E", `?run=${runs[0].id}&run=${runs[0].id}`]) {
    assert.deepEqual(api.readRun(search, runs), {runId:runs.at(-1).id, invalid:true});
  }
  assert.throws(()=>api.readRun("",[]), /No published recordings/);
  assert.throws(()=>api.shareRun("missing",runs), /not in the public catalog/);
});
test("recording and case settings restore independently and copied recording links exclude other content", () => {
  const search = `?case=lantern_ios&view=followup&lang=zh&update=1&run=${runs[0].id}&note=private&redirect=https://example.com`;
  const recording = api.readRun(search,runs);
  const review = api.read(search,workflow);
  assert.equal(review.integration,1);
  assert.equal(review.activeTab,"followup");
  assert.equal(review.language,"zh");
  assert.equal(review.updated,true);
  assert.deepEqual(review.invalid,[]);
  assert.equal(recording.runId,runs[0].id);
  const link = new URL(api.shareRun(recording.runId,runs));
  assert.deepEqual([...link.searchParams.keys()],["run"]);
  assert.ok(!link.href.includes("private"));
  assert.ok(!new URL(api.share(review,workflow)).searchParams.has("run"));
});
test("every published case round-trips across views, languages and update branches", () => {
  workflow.packets.forEach((packet, selected) =>
    packet.integrations.forEach((item, integration) => {
      for (const activeTab of ["evidence", "followup", "handoff"])
        for (const language of ["en", "zh"])
          for (const updated of [false, true]) {
            const state = {
              selected,
              integration,
              activeTab,
              language,
              updated,
            };
            const restored = api.read(
              new URL(api.share(state, workflow)).search,
              workflow,
            );
            assert.deepEqual(restored, { ...state, invalid: [] });
          }
    }),
  );
});
test("an unknown platform cannot select a different customer's evidence", () => {
  const route = api.read("?case=not-a-platform&view=handoff&lang=zh", workflow);
  assert.equal(route.selected, 0);
  assert.equal(route.integration, 0);
  assert.deepEqual(route.invalid, ["case"]);
  assert.equal(route.activeTab, "handoff");
  assert.equal(route.language, "zh");
});
test("invalid or duplicated settings fall back instead of choosing ambiguous values", () => {
  const route = api.read(
    "?case=lantern_ios&case=lantern_android&view=followup&view=handoff&lang=zh&lang=en&update=1&update=0",
    workflow,
  );
  assert.deepEqual(route, {
    ...api.read("", workflow),
    invalid: ["case", "view", "lang", "update"],
  });
  const invalid = api.read("?view=%3Cscript%3E&lang=fr&update=true", workflow);
  assert.deepEqual(invalid.invalid, ["view", "lang", "update"]);
  assert.equal(invalid.updated, false);
});
test("share links contain only allowlisted display settings on the public origin", () => {
  const route = api.read(
    "?case=lantern_ios&view=followup&lang=zh&note=private-text&redirect=https://example.com&v=old",
    workflow,
  );
  const link = new URL(
    api.share(
      { ...route, notes: "do not share", localPath: "C:/Users/private" },
      workflow,
    ),
  );
  assert.equal(link.origin, "https://yuchi-wang02.github.io");
  assert.equal(link.pathname, "/csm-copilot/");
  assert.deepEqual([...link.searchParams.keys()], ["case", "view", "lang"]);
  assert.equal(link.hash, "#workspace");
  assert.ok(!link.href.includes("private"));
});
test("empty URLs restore the original review and invalid internal state cannot be shared", () => {
  assert.deepEqual(api.read("", workflow), {
    selected: 0,
    integration: 0,
    activeTab: "evidence",
    language: "en",
    updated: false,
    invalid: [],
  });
  assert.throws(
    () => api.share({ selected: 99, integration: 0 }, workflow),
    /not in the public workflow/,
  );
  assert.throws(
    () => api.share({ ...api.read("", workflow), activeTab: "send" }, workflow),
    /Invalid review state/,
  );
});
