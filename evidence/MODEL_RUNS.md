# Recorded local model runs

AI-assisted comparison with recorded tool results; not independent human review

Fifteen exploratory attempts across four prescribed tasks, with changed prompts, response contracts, output caps and generation settings. This is not an independent benchmark or a fair model ranking. Tool coverage and matching structured fields do not establish the truth of source records or correctness of free prose. No output is approved for customer use.

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

## Qwen3-4B · queue-first morning review

**Review verdict:** Invented identifiers; five-action batch rejected.
The task supplied no account or integration IDs. The model proposed a queue lookup together with dependent calls using unsupported IDs, in a five-action batch. The four-action limit rejected the entire response before any tool executed. No queue was retrieved and no follow-up or handoff was prepared.

**Task:** Use the fixed synthetic snapshot to find non-live accounts strictly more than three days since recorded contact, including unknown contact history. From the returned queue, select the first account under its planned-launch ordering. Retrieve that account's context, check each of its integrations and prepare an English follow-up for each. Prepare a handoff for each recorded issue on that account. Then explain in at most 220 words why it was selected, how its platform next steps differ, and what is missing from its handoffs. Cite source IDs for recorded facts. Keep missing evidence separate from recorded failures; do not imply launch approval, a confirmed cause or issue resolution. State that nothing was sent or submitted.

Observed requested tool actions: 0/7. Final response present: False.
[Complete trace](model-runs/qwen4-morning-review.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **format: Five proposed actions exceed the batch limit.** The recorded response is a JSON array of five actions. The host accepts at most four and rejected the whole array. The list\_accounts proposal was not executed; it cannot count as completed queue selection.
- **unsupported: Dependent calls used identifiers before discovery.** The model supplied account\_id=12345, integration\_id=67890 and issue\_id=12345 in the first response, before any tool result. These identifiers were absent from the task and are not in the synthetic fixture. Batch-size rejection was the actual stopping condition; no identifier-validation error was returned by a tool.
- **incomplete: Zero of seven requested actions observed.** The fixed-fixture coverage check expects the snapshot queue, its first account context, both platform readiness checks, both English drafts and the recorded issue handoff. None executed; final=null. Coverage does not test dependency order or prove the quality of an explanation.
- **boundary: One uncorrected development attempt.** The run used the existing cached Qwen3-4B revision, 768 generated tokens per turn, an eight-turn cap and zero corrections. It stopped on turn one after 97 generated tokens, without reaching the token cap. This is a preserved failure on a newly authored task, not a model ranking or evidence that queue-first orchestration works.
## Qwen3-4B · morning review with dependency instruction

**Review verdict:** Dependency instruction did not prevent the rejected batch.
The same morning task was repeated with an explicit instruction to call the queue alone and wait for returned IDs before dependent work. The model still proposed five actions with unsupported identifiers. The unchanged four-action limit rejected the entire response; zero tools executed and no final explanation was produced.

**Task:** Use the fixed synthetic snapshot to find non-live accounts strictly more than three days since recorded contact, including unknown contact history. From the returned queue, select the first account under its planned-launch ordering. Retrieve that account's context, check each of its integrations and prepare an English follow-up for each. Prepare a handoff for each recorded issue on that account. Then explain in at most 220 words why it was selected, how its platform next steps differ, and what is missing from its handoffs. Cite source IDs for recorded facts. Keep missing evidence separate from recorded failures; do not imply launch approval, a confirmed cause or issue resolution. State that nothing was sent or submitted.

Observed requested tool actions: 0/7. Final response present: False.
[Complete trace](model-runs/qwen4-morning-sequenced.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **control: Only a dependency paragraph was added to the initial model input.** The user task, available tool schemas, model revision, runtime sampling settings, eight-turn cap and zero-correction budget match the preceding morning recording. The system message adds an instruction to retrieve the queue alone, wait for context and use only IDs in previous results. This is a prompt change, not an enforced state machine or schema constraint.
- **format: The five-action pattern persisted.** The model again proposed list\_accounts, get\_account\_context, check\_readiness, draft\_followup and draft\_ticket together. Its first four proposals match the earlier response. The issue placeholder changed from 12345 to 11223; neither is a fixture issue ID. The host stopped at the same batch-size validation before executing even the queue lookup.
- **incomplete: Coverage remained zero of seven.** No queue or account context was retrieved, no platform or issue call executed, and final=null. The response used 97 tokens without hitting the cap. There was no correction feedback, automatic action repair or successful account discovery.
- **boundary: Prompt presence is not behavioral enforcement.** This paired development observation shows that the added instruction was insufficient in this run. It does not estimate a general failure rate, compare models or prove that all dependency prompts fail. A future enforced call policy would need separate implementation and testing; it is not present in this recording.
## Qwen3-4B · morning review with host policy

**Review verdict:** Parser stopped the proposal before dependency validation.
With the dependency policy enabled, the host supplied a state message allowing only the snapshot queue lookup. The model still proposed five actions and unsupported IDs. The existing four-action parser rejected the response before policy validation or tool execution. Coverage remains 0/7; there is no final explanation.

**Task:** Use the fixed synthetic snapshot to find non-live accounts strictly more than three days since recorded contact, including unknown contact history. From the returned queue, select the first account under its planned-launch ordering. Retrieve that account's context, check each of its integrations and prepare an English follow-up for each. Prepare a handoff for each recorded issue on that account. Then explain in at most 220 words why it was selected, how its platform next steps differ, and what is missing from its handoffs. Cite source IDs for recorded facts. Keep missing evidence separate from recorded failures; do not imply launch approval, a confirmed cause or issue resolution. State that nothing was sent or submitted.

Observed requested tool actions: 0/7. Final response present: False.
[Complete trace](model-runs/qwen4-morning-enforced.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **control: A host state message supplied the allowed next action.** The initial system message, task, schemas, model revision, runtime settings, eight-turn limit and zero-correction budget match the original morning attempt. Unlike that attempt, this run enables the runtime policy and appends an exact pending-action message before generation. It permits only list\_accounts with the fixed snapshot defaults. The prompt-only sequence-dependencies flag is false. This is explicit host planning assistance, not an isolated test of enforcement without an input change.
- **format: The same batch-size error occurred before policy validation.** The model proposed five actions in one array, including account\_12345, integration\_67890 and issue\_12345 before any result. The parser stopped at 'An action batch must contain 1..4 actions'. There is no policy\_error or tool call. It would be incorrect to describe this recording as an observed ID rejection by the new policy.
- **incomplete: The policy remained at awaiting\_queue.** The final policy state matches the state supplied before generation: one pending queue call, no completed actions, no selected account, final\_allowed=false. The 110-token response did not reach the 768-token cap. No correction, retry, queue discovery or final explanation followed.
- **boundary: Software enforcement does not establish successful model use.** The policy's real-MCP scripted integration tests verify call-sequencing boundaries. This separate model run shows that presenting pending actions did not produce a valid first proposal in this attempt. The original twelve raw traces remain unchanged. This is a development observation, not a general failure rate or evidence of autonomous CSM task completion.
## Qwen3-4B · constrained morning workflow

**Review verdict:** Seven tool calls completed; final response timed out.
With host-derived schemas restricting each turn to one pending action, the model completed the snapshot queue, selected account context, both readiness checks, both English drafts and the issue handoff. The host then timed out waiting for the final response. Coverage is 7/7, but no model-written explanation was captured or reviewed.

**Task:** Use the fixed synthetic snapshot to find non-live accounts strictly more than three days since recorded contact, including unknown contact history. From the returned queue, select the first account under its planned-launch ordering. Retrieve that account's context, check each of its integrations and prepare an English follow-up for each. Prepare a handoff for each recorded issue on that account. Then explain in at most 220 words why it was selected, how its platform next steps differ, and what is missing from its handoffs. Cite source IDs for recorded facts. Keep missing evidence separate from recorded failures; do not imply launch approval, a confirmed cause or issue resolution. State that nothing was sent or submitted.

Observed requested tool actions: 7/7. Final response present: False.
[Complete trace](model-runs/qwen4-morning-constrained.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

[Separate host terminal observation](host-observations/qwen4-morning-constrained.json).

- **control: The host constrained the action space on every returned turn.** The model revision, runtime sampling settings, task, initial system input and schemas, eight-turn cap and zero-correction budget match the preceding policy-enabled run. This attempt adds constrained decoding and changes the state instruction to exactly one pending action. The host supplies allowed tool/ID combinations and removes completed work. This is assisted orchestration, not unaided model planning or a clean measurement of one isolated factor.
- **execution: Seven requested calls completed in dependency order.** The model first requested list\_accounts with default arguments, then context for the returned first account acc\_014. It checked Android and iOS, prepared one English follow-up for each, and drafted the recorded issue\_blank handoff. All seven MCP calls returned without tool errors. The final policy state is complete with no pending actions. Each returned response records schema\_constrained=true; no corrections, retries or silently repaired actions were used.
- **evidence: The prepared artifacts retain distinct platform next steps and missing handoff fields.** Android is blocked with three unknown checks and a recorded failed device check; its English draft requests evidence and a fresh device test. iOS has a scoped checklist\_complete result and a launch-plan review draft, with no approval claim. The handoff remains needs\_information with sdk\_version, time\_window and redacted\_logs missing. These are deterministic tool outputs the model requested, not model-authored final reasoning or verified customer outcomes.
- **incomplete: No final explanation was captured.** The raw trace ends with host\_error and error\_type=ExceptionGroup after seven returned turns, with final=null. Captured process stderr identifies the nested TimeoutError at the existing 180-second worker-response wait; that terminal observation is saved separately. This host version did not persist the eighth-turn request before awaiting its response. There is no final wording to grade for source citations, selection rationale, word limit or unsupported promises.
- **boundary: Completion of tool work is not completion of the answer.** Recorded input length grew from 1,338 to 8,069 tokens across the seven returned turns; generation times ranged from 6.434 to 141.776 seconds. These observations are not a controlled performance benchmark or a causal diagnosis. The decoder and state policy supplied strong assistance. The earlier thirteen raw recordings remain unchanged; this run demonstrates prepared artifacts under constraints, not a successful end-to-end model answer or general reliability.
## Qwen3-4B · morning workflow with longer response budget

**Review verdict:** Seven calls and a final answer; evidence states conflated.
The model completed all seven calls and returned an 80-word explanation. Its final generation took 272.986 seconds under an explicit 600-second response budget. The answer names the three missing handoff fields correctly, but groups an unknown currency-approval state and a recorded failed device check as missing verification. A returned answer is progress, not evidence that the task's reasoning requirements are fully met.

**Task:** Use the fixed synthetic snapshot to find non-live accounts strictly more than three days since recorded contact, including unknown contact history. From the returned queue, select the first account under its planned-launch ordering. Retrieve that account's context, check each of its integrations and prepare an English follow-up for each. Prepare a handoff for each recorded issue on that account. Then explain in at most 220 words why it was selected, how its platform next steps differ, and what is missing from its handoffs. Cite source IDs for recorded facts. Keep missing evidence separate from recorded failures; do not imply launch approval, a confirmed cause or issue resolution. State that nothing was sent or submitted.

Observed requested tool actions: 7/7. Final response present: True.
[Complete trace](model-runs/qwen4-morning-long-budget.json). Model revision: `1cfa9a7208912126459214e8b04321603b3df60c`.

- **control: Longer response budget and durable request tracing.** Host source d5c9f289203da935a3250cd9a125475b4c070f8b adds trace lifecycle persistence and uses --response-timeout-seconds 600 instead of the earlier 180-second default. Model revision, runtime settings, initial messages, task, constrained-action policy, eight-turn cap and zero-correction budget match the preceding constrained attempt. Its seven actions and returned tool results also match. This is one development run, not a controlled speed benchmark or general reliability estimate.
- **execution: Seven scoped calls and a returned final response.** Queue, returned-account context, two readiness checks, two English follow-up drafts and the issue handoff all returned without tool errors. The eighth turn produced a final string after 272.986 seconds, with 9,018 input tokens and 134 generated tokens; no output-cap hit, retries or corrections occurred. The process exited 0. Every request, its SHA-256, lifecycle timestamps and decoder schema are saved in the immutable trace.
- **state\_conflation: missing currency approval and device verification.** The Android result records currency\_approved=unknown with no evidence ID, but device\_verified=not\_met with source lantern\_android\_device\_verified. Grouping both as missing fails to preserve missing evidence versus a recorded failed check. The follow-up explicitly requests a fresh device test and separates that from confirmation of unknown settings. Citing the device record does not make the wording faithful to it.
- **supported: SDK version, time window, and redacted logs.** These correspond exactly to the handoff's missing\_fields: sdk\_version, time\_window and redacted\_logs. The draft remains needs\_information with an unconfirmed cause and sent=false. This is a correct part of the model explanation, not independent verification of the underlying customer records.
- **incomplete: Selection, platform next steps and source coverage.** The account name, October 16 planned date, non-live stage, five-day contact age and iOS checklist-complete status match returned records. The answer does not explicitly explain why this account comes first in the queue or distinguish the Android evidence-request action from the iOS launch-plan-review action. It cites two real IDs, msg\_issue\_blank and lantern\_android\_device\_verified, but omits the available contact and iOS sources. It says 'No evidence was sent or submitted'; the trace separately shows drafts remained unsent. There is no launch-approval, resolved-issue or confirmed-root-cause claim.
- **boundary: Format and execution checks do not validate free prose.** The explanation contains 80 whitespace-separated words, within the requested 220-word limit. The schema permits a nonempty final string and does not check factual support or task completeness. The comparisons are AI-assisted review of one saved response, not independent human validation. No customer outcome, time-saving claim or personal mastery is established; all fourteen earlier recordings remain unchanged.

### Unedited model response — needs review

> The account 'Lantern Games' \(acc\_014\) was selected due to its planned launch on 2026-10-16 and being non-live with 5 days since contact. Its platform-specific next steps differ as Android integration is blocked due to missing currency approval and device verification, while iOS is checklist-complete. Handoffs for the recorded issue 'issue\_blank' are pending missing evidence like SDK version, time window, and redacted logs. No evidence was sent or submitted. Source IDs: 'msg\_issue\_blank' for the issue, 'lantern\_android\_device\_verified' for the Android verification status.

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
