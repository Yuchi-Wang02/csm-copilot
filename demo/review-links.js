/* Share only the public synthetic review selection; never page notes or local paths. */
(function (root) {
  "use strict";
  const publicBase = "https://yuchi-wang02.github.io/csm-copilot/";
  function catalog(workflow) {
    return workflow.packets.flatMap((packet, selected) =>
      packet.integrations.map((item, integration) => ({
        id: item.readiness.integration_id,
        selected,
        integration,
      })),
    );
  }
  function read(search, workflow) {
    const params = new URLSearchParams(search);
    const invalid = [];
    function one(key, fallback, valid) {
      if (!params.has(key)) return fallback;
      const values = params.getAll(key);
      if (values.length !== 1 || !valid(values[0])) {
        invalid.push(key);
        return fallback;
      }
      return values[0];
    }
    const items = catalog(workflow);
    const id = one("case", items[0].id, (value) =>
      items.some((item) => item.id === value),
    );
    const item = items.find((item) => item.id === id);
    return {
      selected: item.selected,
      integration: item.integration,
      activeTab: one("view", "evidence", (value) =>
        ["evidence", "followup", "handoff"].includes(value),
      ),
      language: one("lang", "en", (value) => ["en", "zh"].includes(value)),
      updated:
        one("update", "0", (value) => ["0", "1"].includes(value)) === "1",
      invalid,
    };
  }
  function query(state, workflow) {
    const item = catalog(workflow).find(
      (item) =>
        item.selected === state.selected &&
        item.integration === state.integration,
    );
    if (!item)
      throw new Error("Review selection is not in the public workflow");
    const params = new URLSearchParams({
      case: item.id,
      view: state.activeTab,
      lang: state.language,
    });
    if (state.updated) params.set("update", "1");
    // Normalize through the same allowlist used by incoming URLs.
    const normalized = read(params.toString(), workflow);
    if (normalized.invalid.length) throw new Error("Invalid review state");
    return "?" + params.toString();
  }
  function share(state, workflow) {
    return publicBase + query(state, workflow) + "#workspace";
  }
  const api = { read, query, share };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CSM_REVIEW_LINKS = api;
})(typeof window !== "undefined" ? window : this);
