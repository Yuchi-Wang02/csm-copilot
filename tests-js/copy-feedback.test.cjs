const { test } = require("node:test");
const assert = require("node:assert/strict");
const { create } = require("../demo/copy-feedback.js");

function pendingWrite() {
  let resolve, reject;
  const promise = new Promise((yes, no) => { resolve = yes; reject = no; });
  return { promise, resolve, reject };
}
const button = () => ({ isConnected: true, textContent: "Copy" });

test("copy captures the exact text and reports success after completion", async () => {
  const pending = pendingWrite(), target = button(), values = [];
  const api = create((text) => { values.push(text); return pending.promise; });
  const result = api.copy(target, "中文 draft\n<literal>", "Copied", "Fallback");
  assert.equal(target.textContent, "Copying…");
  assert.deepEqual(values, ["中文 draft\n<literal>"]);
  pending.resolve();
  await result;
  assert.equal(target.textContent, "Copied");
});

test("changing selection invalidates late success and failure feedback", async () => {
  for (const failed of [false, true]) {
    const pending = pendingWrite(), target = button();
    const api = create(() => pending.promise);
    let fallback = 0;
    const result = api.copy(target, "old link", "Copied", "Fallback", () => fallback++);
    api.reset(target, "Copy new link");
    if (failed) pending.reject(new Error("denied")); else pending.resolve();
    await result;
    assert.equal(target.textContent, "Copy new link");
    assert.equal(fallback, 0, "stale failures must not open details or move focus");
  }
});

test("a removed draft button cannot update its replacement or throw", async () => {
  for (const failed of [false, true]) {
    const pending = pendingWrite(), original = button(), replacement = button();
    const api = create(() => pending.promise);
    let fallback = false;
    const result = api.copy(original, "old draft", "Copied", "Fallback", () => { fallback = true; });
    original.isConnected = false;
    if (failed) pending.reject(new Error("denied")); else pending.resolve();
    await result;
    assert.equal(replacement.textContent, "Copy");
    assert.equal(fallback, false);
  }
});

test("only the newest attempt on a button can report its result", async () => {
  const old = pendingWrite(), recent = pendingWrite(), target = button();
  let count = 0, fallback = 0;
  const api = create(() => count++ === 0 ? old.promise : recent.promise);
  const first = api.copy(target, "first", "Old copied", "Old fallback", () => fallback++);
  const second = api.copy(target, "second", "New copied", "New fallback");
  recent.resolve();
  await second;
  old.reject(new Error("late denial"));
  await first;
  assert.equal(target.textContent, "New copied");
  assert.equal(fallback, 0);
});

test("current clipboard denial or unavailable API retains the explicit fallback", async () => {
  for (const write of [() => Promise.reject(new Error("denied")), () => { throw new TypeError("API unavailable"); }]) {
    const target = button();
    let fallback = 0;
    await create(write).copy(target, "link", "Copied", "Select link", () => fallback++);
    assert.equal(target.textContent, "Select link");
    assert.equal(fallback, 1);
  }
});

test("selection resets do not invalidate a different copy control", async () => {
  const pending = pendingWrite(), one = button(), two = button();
  const api = create(() => pending.promise);
  const result = api.copy(one, "recording link", "Copied", "Fallback");
  api.reset(two, "Copy practice link");
  pending.resolve();
  await result;
  assert.equal(one.textContent, "Copied");
  assert.equal(two.textContent, "Copy practice link");
});
