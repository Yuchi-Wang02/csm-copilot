# Recorded local model runs

AI-assisted comparison with recorded tool results; not independent human review

Exploratory attempts on one task with changed prompts, response contracts, output caps and generation settings. This is not an independent benchmark or a fair model ranking. Tool coverage and matching structured fields do not establish the truth of source records or correctness of free prose. No output is approved for customer use.

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

## Qwen3-4B · structured final, no correction

**Review verdict:** Structured response rejected before field review.
The model completed the four tools, but its nested final JSON was malformed. No structured-field match is claimed.

Observed requested tool actions: 4/4. Final response present: False.
[Complete trace](model-runs/qwen4-grounded.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **format: Missing closing object delimiter.** The parser rejected the model output. The raw response also includes an issue-only source in the readiness evidence list, but no automated field review was reached.
## Qwen3-4B · two correction requests

**Review verdict:** Correction budget exhausted.
After the four tool calls, the model repeated the malformed final response through both recorded correction requests. The host stopped without accepting it.

Observed requested tool actions: 4/4. Final response present: False.
[Complete trace](model-runs/qwen4-grounded-corrections.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **observed: Two requests did not fix the JSON.** The trace preserves the original output and both correction responses. The model did not reach a parseable structured final; no field-match result or approved explanation is claimed.
## Qwen3-4B · constrained JSON \+ field review

**Review verdict:** Structured fields match after two corrections.
Four requested tools executed. Schema-constrained finals first failed source and platform-scope checks. After two recorded correction requests, the declared fields matched the observed results. Free prose remains unverified.

Observed requested tool actions: 4/4. Final response present: True.
[Complete trace](model-runs/qwen4-constrained.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **rejected: Issue-only evidence and duplicate platform entries.** The first constrained final included msg\_issue\_blank as readiness evidence and repeated Android entries. The next response still repeated platform entries. Both were rejected; the raw outputs and feedback remain in the trace.
- **matched: Final structured fields match tool evidence.** The last response contains both platforms exactly once, preserves the Android unknown checks and device failure, cites the expected readiness IDs, and keeps nothing\_sent=true and launch\_approved=false. Feedback supplied expected values; this is an assisted correction result on one task, not independent accuracy.
- **limited: Free explanation is not verified.** The final explanation describes the platform difference but omits inline source IDs and the explicit nothing-sent sentence requested in the task. Those facts appear in structured fields and the separate system-rendered summary. A field match does not establish full instruction compliance.

Structured review: **structured_fields_match**. Free explanation: **not semantically verified**.

### System-rendered summary from checked tool fields

> Moon Garden / Android: blocked.
> - Platform currency approval: unknown \[no applicable record\].
> - Production visibility setting: unknown \[no applicable record\].
> - Placement and content: met \[lantern\_android\_placement\_linked\].
> - SDK connection sequence: met \[lantern\_android\_sdk\_connected\].
> - Non-test device verification: not\_met \[lantern\_android\_device\_verified\].
> - Reward callback verification: unknown \[no applicable record\].
> Proposed next action: Review and send the evidence request, then reassess when new records arrive.
> Moon Garden / iOS: checklist\_complete.
> - Platform currency approval: met \[lantern\_ios\_currency\_approved\].
> - Production visibility setting: met \[lantern\_ios\_test\_only\_off\].
> - Placement and content: met \[lantern\_ios\_placement\_linked\].
> - SDK connection sequence: met \[lantern\_ios\_sdk\_connected\].
> - Non-test device verification: met \[lantern\_ios\_device\_verified\].
> - Reward callback verification: met \[lantern\_ios\_callback\_verified\].
> Proposed next action: Review the launch plan and confirm any changes since the recorded checks.
> Nothing was sent. This scoped checklist does not grant launch approval.

### Unedited model response — needs review

> Lantern Android requires evidence for currency approval, Test Only status, and callback verification, with a failed device verification. Lantern iOS has a complete checklist but no unknown checks. The follow-ups differ because Android needs additional evidence while iOS is ready for launch review.

Narrow promise lint flags: []. No flags does not establish fidelity.
