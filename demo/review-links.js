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
    const result = {
      selected: item.selected,
      integration: item.integration,
      activeTab: one("view", "evidence", (value) =>
        ["evidence", "followup", "handoff"].includes(value),
      ),
      language: one("lang", "en", (value) => ["en", "zh"].includes(value)),
      updated:
        one("update", "0", (value) => ["0", "1", "2"].includes(value)) !== "0",
      invalid,
    };
    result.verified = result.updated && params.get("update") === "2";
    return result;
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
    if (state.verified && !state.updated) throw new Error("Invalid review state");
    if (state.updated) params.set("update", state.verified ? "2" : "1");
    // Normalize through the same allowlist used by incoming URLs.
    const normalized = read(params.toString(), workflow);
    if (normalized.invalid.length) throw new Error("Invalid review state");
    return "?" + params.toString();
  }
  function share(state, workflow) {
    return publicBase + query(state, workflow) + "#workspace";
  }
  function readRun(search, runs) {
    if (!runs.length) throw new Error("No published recordings available");
    const values = new URLSearchParams(search).getAll("run");
    const valid = values.length === 1 && runs.some((run) => run.id === values[0]);
    return {
      runId: valid ? values[0] : runs.at(-1).id,
      invalid: values.length > 0 && !valid,
    };
  }
  function runQuery(runId, runs) {
    if (!runs.some((run) => run.id === runId))
      throw new Error("Recording is not in the public catalog");
    return "?" + new URLSearchParams({ run: runId }).toString();
  }
  function shareRun(runId, runs) {
    return publicBase + runQuery(runId, runs) + "#model-runs";
  }
  function readProbe(search, probes) {
    if (!probes.length) throw new Error("No published triage probes available");
    const values = new URLSearchParams(search).getAll("probe");
    const valid = values.length === 1 && probes.some((probe) => probe.id === values[0]);
    return {
      probeId: valid ? values[0] : probes[0].id,
      invalid: values.length > 0 && !valid,
    };
  }
  function probeQuery(probeId, probes) {
    if (!probes.some((probe) => probe.id === probeId))
      throw new Error("Triage probe is not in the public catalog");
    return "?" + new URLSearchParams({ probe: probeId }).toString();
  }
  function shareProbe(probeId, probes) {
    return publicBase + probeQuery(probeId, probes) + "#triage-review";
  }
  const api = { read, query, share, readRun, runQuery, shareRun, readProbe, probeQuery, shareProbe };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CSM_REVIEW_LINKS = api;
})(typeof window !== "undefined" ? window : this);
