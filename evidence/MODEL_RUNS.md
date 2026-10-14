# Recorded local model runs

AI-assisted comparison with recorded tool results; not independent human review

Three exploratory runs on one task, with a changed host protocol after observed failures. This is neither an independent benchmark nor a fair model ranking. Tool coverage is not answer correctness. No output is approved for customer use.

## Qwen3-0.6B · single-action smoke

**Review verdict:** Stopped before tool execution.
The model wrapped its action in Markdown fences and invented a 2023 date. Strict parsing rejected the response; no tool was called.

Observed requested tool actions: 0/4. Final response present: False.
[Complete trace](model-runs/qwen06-single.json). Model revision: `c1899de289a04d12100db370d81485cdf75e47ca`.

- **format: Markdown-fenced JSON.** The requested protocol accepts plain JSON only. The host did not silently strip the fences.
- **unsupported: as\_of: 2023-04-01.** The task did not supply this date. The dataset snapshot is 2026-10-14; the action was rejected before reaching the tool.
## Qwen3-4B · single-action attempt

**Review verdict:** Stopped before tool execution.
The model selected four relevant calls but emitted concatenated JSON objects. The one-action protocol rejected the whole output; zero calls executed.

Observed requested tool actions: 0/4. Final response present: False.
[Complete trace](model-runs/qwen4-single.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **format: Four concatenated JSON objects.** Relevant proposed tool choices are visible, but they were not executed. This led to an explicit bounded-array protocol in the next run, not a hidden repair of this output.
## Qwen3-4B · explicit batch protocol

**Review verdict:** Final explanation needs revision.
All four requested tool calls executed, but the final explanation omitted citations, overstated the iOS result, and blurred a recorded Android failure into missing evidence.

Observed requested tool actions: 4/4. Final response present: True.
[Complete trace](model-runs/qwen4-batch.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **unsupported: iOS's full compliance.** The tool reports checklist\_complete for six scoped checks and explicitly says it is not launch approval. Compliance was not evaluated.
- **contradicted: No evidence IDs are missing for Android.** Android currency approval, production visibility and callback verification have unknown states with empty evidence\_ids. No source IDs are cited in the final explanation.
- **omitted: Android's missing evidence.** This is incomplete: lantern\_android\_device\_verified supports a not\_met state. The final explanation fails to distinguish the recorded failed check from the unknown checks.
- **supported: Nothing was sent.** Both follow-up tool outputs have sent=false and contact\_history\_changed=false. The server exposes no sending capability.

### Unedited model response — needs review

> Lantern Android requires confirmation on currency approval, Test Only status, and a non-test device check, along with a callback example. Lantern iOS has a complete checklist but needs confirmation of no changes and current launch plans. The differences arise from Android's missing evidence and iOS's full compliance. No evidence IDs are missing for Android, while iOS has all required evidence. Nothing was sent.

Narrow promise lint flags: []. No flags does not establish fidelity.
