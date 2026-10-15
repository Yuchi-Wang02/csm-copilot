/* Local, user-editable practice checkpoints. Never import evidence or guidance. */
(function (root) {
  "use strict";
  const FORMAT = "csm-practice-progress-v1";
  const MAX_BYTES = 512 * 1024;
  const fail = (message) => { throw new Error(message); };
  function keys(value, expected) {
    if (!value || typeof value !== "object" || Array.isArray(value) ||
        Object.keys(value).length !== expected.length ||
        !expected.every((key) => Object.prototype.hasOwnProperty.call(value, key)))
      fail("The progress file has an unsupported structure.");
  }
  function note(value) {
    if (typeof value !== "string" || value.length > 4000)
      fail("Each saved note must be text of at most 4,000 characters.");
    return value;
  }
  function validateItems(items, cases) {
    if (!Array.isArray(items) || items.length !== cases.length)
      fail("The progress file must contain each current decision exactly once.");
    const byId = new Map();
    for (const item of items) {
      keys(item, ["id", "choice", "reasoning", "reviewed", "initial", "reflection"]);
      const decision = cases.find((c) => c.id === item.id);
      if (!decision || byId.has(item.id)) fail("A saved decision is unknown or repeated.");
      if (typeof item.reviewed !== "boolean" || typeof item.choice !== "string" ||
          (item.choice !== "" && !decision.options.some((o) => o.id === item.choice)))
        fail("A saved decision has an invalid choice or review state.");
      const reasoning = note(item.reasoning), reflection = note(item.reflection);
      let initial = null;
      if (item.reviewed) {
        keys(item.initial, ["choice", "reasoning"]);
        if (!item.choice || item.initial.choice !== item.choice || note(item.initial.reasoning) !== reasoning)
          fail("The saved original response is inconsistent with its reviewed decision.");
        initial = { choice: item.choice, reasoning };
      } else if (item.initial !== null || reflection !== "") {
        fail("An unfinished decision cannot include a reviewed response or later reflection.");
      }
      byId.set(item.id, { id: item.id, choice: item.choice, reasoning, reviewed: item.reviewed, initial, reflection });
    }
    return cases.map((c) => byId.get(c.id));
  }
  async function signature(cases) {
    // Detect changed exercise content, not authorship or tampering. IDs survive reordering.
    const catalog = cases.map((c) => ({
      id: c.id, title: c.title, situation: c.situation, evidence: c.evidence,
      options: [...c.options].sort((a, b) => a.id.localeCompare(b.id)),
      expected: c.expected, source: c.source, sourceLabel: c.sourceLabel,
      explanation: c.explanation, prompt: c.prompt,
    })).sort((a, b) => a.id.localeCompare(b.id));
    const bytes = new TextEncoder().encode(JSON.stringify(catalog));
    const digest = await crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, "0")).join("");
  }
  async function save(cases, session, selectedId, asOf) {
    const items = validateItems(session, cases);
    if (!cases.some((c) => c.id === selectedId)) fail("Select a current practice decision first.");
    const file = {
      format: FORMAT,
      snapshot: asOf,
      exercise_signature: await signature(cases),
      selected_id: selectedId,
      items,
    };
    return JSON.stringify(file, null, 2) + "\n";
  }
  async function load(content, cases, asOf) {
    if (typeof content !== "string" || new TextEncoder().encode(content).length > MAX_BYTES)
      fail("Choose a progress JSON file no larger than 512 KiB.");
    let file;
    try { file = JSON.parse(content); } catch { fail("This is not a valid progress JSON file. Markdown notes cannot restore progress."); }
    keys(file, ["format", "snapshot", "exercise_signature", "selected_id", "items"]);
    if (file.format !== FORMAT) fail("This progress-file version is not supported.");
    if (!Array.isArray(file.items) || !file.items.length)
      fail("The progress file must contain saved decisions.");
    const savedIds = file.items.map((item) => item?.id);
    if (new Set(savedIds).size !== savedIds.length || savedIds.some((id) => !cases.some((c) => c.id === id)))
      fail("A saved decision is unknown or repeated.");
    const savedCases = cases.filter((c) => savedIds.includes(c.id));
    const savedSession = validateItems(file.items, savedCases);
    if (file.snapshot !== asOf || file.exercise_signature !== await signature(savedCases))
      fail("These saved responses use different exercise content. Keep them as a record; they cannot be resumed against this version.");
    if (!savedIds.includes(file.selected_id)) fail("The saved selected decision is unavailable.");
    const addedDecisionIds = cases.filter((c) => !savedIds.includes(c.id)).map((c) => c.id);
    const session = cases.map((c) => savedSession.find((item) => item.id === c.id) ||
      {id: c.id, choice: "", reasoning: "", reviewed: false, initial: null, reflection: ""});
    return { session, selectedId: file.selected_id, addedDecisionIds };
  }
  const api = { MAX_BYTES, save, load };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CSM_PRACTICE_SESSION = api;
})(typeof window !== "undefined" ? window : this);
