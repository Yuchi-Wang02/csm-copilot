# Recorded local model runs

AI-assisted comparison with recorded tool results; not independent human review

Eight exploratory attempts across two prescribed tasks, with changed prompts, response contracts, output caps and generation settings. This is not an independent benchmark or a fair model ranking. Tool coverage and matching structured fields do not establish the truth of source records or correctness of free prose. No output is approved for customer use.

## Qwen3-0.6B · single-action smoke

**Review verdict:** Stopped before tool execution.
The model wrapped its action in Markdown fences and invented a 2023 date. Strict parsing rejected the response; no tool was called.

**Task:** Review Lantern Games' two integrations: lantern\_android and lantern\_ios. Use tools to check readiness for each and prepare an English follow-up for each. Then explain in at most 180 words why the two follow-ups differ. Cite evidence IDs for recorded facts; say when evidence is missing. Do not promise launch approval. State that nothing was sent.

Observed requested tool actions: 0/4. Final response present: False.
[Complete trace](model-runs/qwen06-single.json). Model revision: `c1899de289a04d12100db370d81485cdf75e47ca`.

- **format: Markdown-fenced JSON.** The requested protocol accepts plain JSON only. The host did not silently strip the fences.
- **unsupported: as\_of: 2023-04-01.** The task did not supply this date. The dataset snapshot is 2026-10-14; the action was rejected before reaching the tool.
## Qwen3-4B · single-action attempt

**Review verdict:** Stopped before tool execution.
The model selected four relevant calls but emitted concatenated JSON objects. The one-action protocol rejected the whole output; zero calls executed.

**Task:** Review Lantern Games' two integrations: lantern\_android and lantern\_ios. Use tools to check readiness for each and prepare an English follow-up for each. Then explain in at most 180 words why the two follow-ups differ. Cite evidence IDs for recorded facts; say when evidence is missing. Do not promise launch approval. State that nothing was sent.

Observed requested tool actions: 0/4. Final response present: False.
[Complete trace](model-runs/qwen4-single.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **format: Four concatenated JSON objects.** Relevant proposed tool choices are visible, but they were not executed. This led to an explicit bounded-array protocol in the next run, not a hidden repair of this output.
## Qwen3-4B · explicit batch protocol

**Review verdict:** Final explanation needs revision.
All four requested tool calls executed, but the final explanation omitted citations, overstated the iOS result, and blurred a recorded Android failure into missing evidence.

**Task:** Review Lantern Games' two integrations: lantern\_android and lantern\_ios. Use tools to check readiness for each and prepare an English follow-up for each. Then explain in at most 180 words why the two follow-ups differ. Cite evidence IDs for recorded facts; say when evidence is missing. Do not promise launch approval. State that nothing was sent.

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

**Task:** Review Lantern Games' two integrations: lantern\_android and lantern\_ios. Use tools to check readiness for each and prepare an English follow-up for each. Then explain in at most 180 words why the two follow-ups differ. Cite evidence IDs for recorded facts; say when evidence is missing. Do not promise launch approval. State that nothing was sent.

Observed requested tool actions: 4/4. Final response present: False.
[Complete trace](model-runs/qwen4-grounded.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **format: Missing closing object delimiter.** The parser rejected the model output. The raw response also includes an issue-only source in the readiness evidence list, but no automated field review was reached.
## Qwen3-4B · two correction requests

**Review verdict:** Correction budget exhausted.
After the four tool calls, the model repeated the malformed final response through both recorded correction requests. The host stopped without accepting it.

**Task:** Review Lantern Games' two integrations: lantern\_android and lantern\_ios. Use tools to check readiness for each and prepare an English follow-up for each. Then explain in at most 180 words why the two follow-ups differ. Cite evidence IDs for recorded facts; say when evidence is missing. Do not promise launch approval. State that nothing was sent.

Observed requested tool actions: 4/4. Final response present: False.
[Complete trace](model-runs/qwen4-grounded-corrections.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **observed: Two requests did not fix the JSON.** The trace preserves the original output and both correction responses. The model did not reach a parseable structured final; no field-match result or approved explanation is claimed.
## Qwen3-4B · constrained JSON \+ field review

**Review verdict:** Structured fields match after two corrections.
Four requested tools executed. Schema-constrained finals first failed source and platform-scope checks. After two recorded correction requests, the declared fields matched the observed results. Free prose remains unverified.

**Task:** Review Lantern Games' two integrations: lantern\_android and lantern\_ios. Use tools to check readiness for each and prepare an English follow-up for each. Then explain in at most 180 words why the two follow-ups differ. Cite evidence IDs for recorded facts; say when evidence is missing. Do not promise launch approval. State that nothing was sent.

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

## Qwen3-4B · callback handoff task

**Review verdict:** Handoff facts partly preserved; scope and ownership need review.
A second task: two requested tool actions completed, plus two extra calls. The answer cites the issue source and names both missing fields, but blurs a failed check with an unconfirmed cause and omits the proposed owner. No correction requests were made.

**Task:** Review Harbor Studio \(account acc\_006\) and its recorded issue issue\_callback. Retrieve the account context and prepare the issue handoff using tools. Then explain in at most 180 words the reported observation, any hypothesis that remains unconfirmed, the missing handoff fields, and the proposed next owner and action. Cite evidence IDs for recorded facts. Do not claim the cause is confirmed, the issue is resolved, or a ticket was submitted. State that nothing was sent.

Observed requested tool actions: 2/2. Final response present: True.
[Complete trace](model-runs/qwen4-callback-handoff.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **supported: HTTP 405, Japan, missing fields and issue citation.** The answer reports the recorded symptom and region, names reproduction steps and redacted logs, cites msg\_issue\_callback, and says no ticket was submitted. These statements agree with the handoff output.
- **mismatched: The callback\_verified status is unconfirmed.** The account context records callback\_verified as not\_met, supported by harbor\_android\_callback\_verified. The root cause is unconfirmed. Combining these separate states obscures an observed failure.
- **omitted: Proposed owner and specific unconfirmed hypothesis.** The answer omits Technical support after CSM evidence review and the endpoint-method-mismatch hypothesis. It says no ticket was submitted, but does not explicitly state that nothing was sent as the task requested.
- **input error: Triage receives an identifier instead of customer prose.** The extra triage\_issue call receives issue\_text="issue\_callback" and no integration scope. A lexical match retrieves the callback category, but this is not evidence that the customer message was triaged. The separate draft\_ticket call correctly uses the recorded issue and supplies its actual summary.

### Unedited model response — needs review

> Harbor Studio \(acc\_006\) reported a reward callback issue with HTTP 405 in Japan. The callback\_verified status is unconfirmed. Missing fields include reproduction steps and redacted logs. The issue is unconfirmed, and no ticket was submitted. Next action: request missing evidence and review the handoff. Evidence ID: msg\_issue\_callback.

Narrow promise lint flags: []. No flags does not establish fidelity.

## Qwen3-4B · handoff with identifier check

**Review verdict:** Bad triage input rejected; final answer still incomplete.
The same initial four-call batch repeats the issue-ID input error. The server rejects that extra call, while both requested actions succeed. The answer separates the failed check from the unconfirmed cause and states nothing was sent, but omits evidence IDs, the proposed owner and the specific hypothesis.

**Task:** Review Harbor Studio \(account acc\_006\) and its recorded issue issue\_callback. Retrieve the account context and prepare the issue handoff using tools. Then explain in at most 180 words the reported observation, any hypothesis that remains unconfirmed, the missing handoff fields, and the proposed next owner and action. Cite evidence IDs for recorded facts. Do not claim the cause is confirmed, the issue is resolved, or a ticket was submitted. State that nothing was sent.

Observed requested tool actions: 2/2. Final response present: True.
[Complete trace](model-runs/qwen4-callback-input-guard.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **rejected: Known issue ID passed as customer prose.** The model again sends issue\_text="issue\_callback". In project version 0.9.1 the server returns a tool error with guidance to retrieve the customer message or use draft\_ticket. The model does not retry triage. Its valid draft\_ticket call separately supplies the actual recorded issue.
- **supported: Failed check, causal uncertainty and nothing sent.** The final response preserves callback\_verified=not\_met separately from the unconfirmed root cause. HTTP 405, region, SDK version, time window, missing fields and the draft state agree with the returned records. It explicitly says nothing was sent.
- **omitted: Evidence citations, owner and specific hypothesis.** The answer names account, issue and draft IDs but does not cite msg\_issue\_callback or the readiness evidence IDs requested by the task. It also omits Technical support after CSM evidence review and the endpoint-method-mismatch hypothesis. These gaps prevent a claim of full task completion.
- **boundary: A repeated task after a tool-contract change.** One fresh generation used the same task and sampling configuration, but the tool description and error behavior changed. The first action batch matches the earlier recording. No host correction requests were sent. This is an observed development iteration, not a controlled estimate of general improvement or independent human validation.

### Unedited model response — needs review

> Harbor Studio \(acc\_006\) has a recorded issue \(issue\_callback\) with Android's reward callback returning HTTP 405. The issue was observed in Japan with SDK synthetic-version-1 between 08:30–09:00 UTC on 2026-10-10. Evidence shows callback\_verified is not\_met, but other checks like currency\_approved, device\_verified, and sdk\_connected are met. The root cause remains unconfirmed, and missing fields include reproduction\_steps and redacted\_logs. A draft ticket \(ticket-issue\_callback\) was prepared but not sent. Next action: request missing evidence and review the handoff before submitting a ticket. Nothing was sent.

Narrow promise lint flags: []. No flags does not establish fidelity.
