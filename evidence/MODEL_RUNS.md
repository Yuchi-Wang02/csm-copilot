# Recorded local model runs

AI-assisted comparison with recorded tool results; not independent human review

Ten exploratory attempts across three prescribed tasks, with changed prompts, response contracts, output caps and generation settings. This is not an independent benchmark or a fair model ranking. Tool coverage and matching structured fields do not establish the truth of source records or correctness of free prose. No output is approved for customer use.

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

## Qwen3-4B · two inbound messages

**Review verdict:** Correct tool split; invoice questions still generic.
The model triages both exact messages with no invented integration, proposes different next actions and states that nothing was sent. Its invoice follow-up repeats generic app/platform troubleshooting questions. The response needs a CSM review for customer fit and clearer candidate-versus-diagnosis wording.

**Task:** Review two unrelated synthetic inbound messages. No account or integration ID has been provided. Message A: Please send the blanket invoice for our annual plan. Message B: The offerwall is blank on Android. Use triage\_issue on each exact original message separately, without assigning an integration. Then explain in at most 200 words one proposed next action and two customer clarification questions for each message. Distinguish a retrieved candidate from a confirmed diagnosis. Refer to the tool's route for each message. Do not invent account IDs, evidence IDs, company procedures or a confirmed owner outside the tool results. State that nothing was sent.

Observed requested tool actions: 2/2. Final response present: True.
[Complete trace](model-runs/qwen4-triage-scope.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **supported: Both messages preserved without invented identity.** Two successful triage\_issue calls use the exact task messages and integration\_id=null. The invoice returns unknown / clarify\_scope; the blank Offerwall returns no\_offers / collect\_evidence. There are no extra calls, retries or host correction requests.
- **supported: Different proposed actions and nothing sent.** The answer asks for clarification on Message A and proposes currency-setting evidence and a device comparison for Message B. Those actions reflect the returned routes. It supplies two clarification prompts for each message and explicitly says nothing was sent; it does not invent account or evidence IDs.
- **needs review: Invoice questions repeat a generic technical fallback.** For the invoice request, the answer asks which app/platform is affected and what was expected versus what happened. This follows the tool's unknown-scope fallback, but does little to clarify the requested invoice. This is an AI-assisted editorial assessment of customer fit, not an independently measured quality score or a verified billing workflow.
- **qualification: Tentative wording is present; diagnostic limits could be clearer.** The phrase potential issues avoids stating a confirmed cause, and currency approval and placement are listed candidate checks. However, the answer does not explicitly explain that no\_offers is a lexical retrieval candidate or repeat root\_cause=unconfirmed. The named route codes are not quoted, although its proposed actions reflect them. Human review is still required.
- **boundary: One development task after the lexical repair.** The invoice message reuses a published development probe. One local generation used the batch protocol, a four-step cap and 768-token output cap with no host corrections. This is a third prescribed task, not a held-out evaluation or a controlled estimate of model improvement.

### Unedited model response — needs review

> For Message A: The triage identified 'unknown' category, requiring clarification on the affected app/platform. Next action: Request details on the app and platform. Clarification questions: What app and platform is this for? What was expected vs. what happened? For Message B: The triage identified 'no\_offers' category, suggesting potential issues with currency approval or placement. Next action: Collect evidence on currency settings and device comparison. Clarification questions: Confirm the affected app and platform. Share currency approval and Test Only settings for that platform. Nothing was sent.

Narrow promise lint flags: []. No flags does not establish fidelity.

## Qwen3-4B · neutral scope questions

**Review verdict:** Technical assumption removed; invoice follow-up still broad.
The same task and initial prompt produce the same two tool calls. With neutral unknown-scope questions in the tool result, the answer asks about account/product context and the requested information. Both routes remain correct, and nothing was sent. This one development pair does not establish general improvement.

**Task:** Review two unrelated synthetic inbound messages. No account or integration ID has been provided. Message A: Please send the blanket invoice for our annual plan. Message B: The offerwall is blank on Android. Use triage\_issue on each exact original message separately, without assigning an integration. Then explain in at most 200 words one proposed next action and two customer clarification questions for each message. Distinguish a retrieved candidate from a confirmed diagnosis. Refer to the tool's route for each message. Do not invent account IDs, evidence IDs, company procedures or a confirmed owner outside the tool results. State that nothing was sent.

Observed requested tool actions: 2/2. Final response present: True.
[Complete trace](model-runs/qwen4-triage-neutral-questions.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **supported: Same initial prompt, task, runtime settings and tool actions.** The initial messages and their SHA-256 match the preceding inbound-message recording. Model revision, recorded runtime configuration and initial two-call batch also match. Both calls succeed with exact original messages and integration\_id=null; there are no extra calls, tool errors or host corrections.
- **changed: Only the unknown-candidate questions differ in returned tool data.** The invoice tool result now asks for account/product context and requested information or outcome. All other invoice-result fields match the previous recording, and the complete blank-Offerwall result is unchanged. The historical recording retains its original app/platform question.
- **needs review: Invoice questions no longer assume a technical symptom.** The final answer repeats the two neutral questions rather than asking about app/platform failure. They are still broad: the request already identifies an invoice, and a CSM should tailor the follow-up to relevant account details instead of treating the fallback as a verified billing workflow. This customer-fit assessment is AI-assisted editorial review, not independent validation.
- **qualification: Candidate wording is clearer, but source limits are not fully explained.** The answer calls both outputs candidates, proposes clarification versus evidence collection, and states that nothing was sent. It does not explicitly explain lexical retrieval, repeat root\_cause=unconfirmed or cite the Offerwall source URL. Its actions reflect the tool routes without quoting route codes. Human review remains necessary.
- **boundary: One fresh local attempt, with all earlier recordings retained.** This is the tenth exploratory recording across three prescribed tasks. The invoice message is a published development probe. A matched prompt and sampling configuration do not make a single generated pair a general reliability estimate, a blinded test or independent human review.

### Unedited model response — needs review

> For Message A: The candidate is 'unknown' and requires clarification on the account or product involved. Next action: Request details about the account or product. Questions: 'Which account or product does this request concern?', 'What specific information or outcome do you need, and which relevant details should we review?' For Message B: The candidate is 'no\_offers' with sources. Next action: Collect evidence on currency approval, Test Only settings, placement, SDK connection, and device verification. Questions: 'Confirm the affected app and platform.', 'Share currency approval and Test Only settings for that platform.' Nothing was sent.

Narrow promise lint flags: []. No flags does not establish fidelity.

## Compare the callback handoff attempts

Two development runs of the same task. The tool description and validation behavior changed. These observations are not a causal improvement estimate, benchmark score or independent human review.

- Task text: same.
- Model and revision: same.
- Recorded sampling settings: same.
- Initial action batch: same.
- System message including tool descriptions: different.

| Recorded observation | Earlier run | With identifier check |
|---|---|---|
| Requested actions observed | 2 / 2 | 2 / 2 |
| Total attempted calls | 4 | 4 |
| Tool errors | 0 | 1 |
| Triage input | issue\_callback | issue\_callback |
| Triage result | Accepted | Rejected |

### Source comparison — AI-assisted

| Review point | Earlier answer | Newer answer |
|---|---|---|
| Failed check versus cause | Calls callback\_verified unconfirmed. | Preserves not\_met separately from an unconfirmed root cause. |
| Evidence citations | Cites msg\_issue\_callback. | Names account, issue and draft IDs, but omits source evidence IDs. |
| Owner and specific hypothesis | Both omitted. | Both still omitted. |
| Nothing-sent statement | Says no ticket was submitted. | Explicitly says nothing was sent. |

[Earlier trace](model-runs/qwen4-callback-handoff.json) · [Newer trace](model-runs/qwen4-callback-input-guard.json)
