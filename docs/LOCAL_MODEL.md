# An actual model run, including the failures

The project contains eighteen exploratory local model attempts across four synthetic CSM tasks. Unlike the scripted MCP smoke test, a language model proposed the tool names and arguments. The host executed accepted calls through the real MCP stdio transport and returned their full results to the model. Rejected proposals are retained without being counted as executed calls.

The queue-first sequence separates several failure modes. The first three morning attempts stop before tool execution. Constrained actions then complete seven calls but time out on the final answer. A longer response budget returns prose with evidence-state gaps; structured field review subsequently catches an issue report used as a readiness citation. Reducing the final context preserves that same citation failure. The dated source references and complete recordings below retain each outcome and its host assistance, rather than treating the sequence as a controlled benchmark.

**The initial batch attempt completed four requested tool actions but overstated the evidence. The constrained platform-follow-up run matched structured fields after two corrections; its prose remains unverified.** That distinction is the point of this experiment: tool completion does not establish answer fidelity.

[Inspect the browser replay](https://yuchi-wang02.github.io/csm-copilot/#model-runs) · [Read the reviewed results](../evidence/MODEL_RUNS.md) · [Review annotations](../evidence/model-runs/review.json)

## Initial v0.5 task and observed attempts

The task names Lantern Games' Android and iOS integration IDs, asks for readiness checks and English follow-up drafts for both, then requests a short evidence-citing explanation of why the follow-ups differ. It also requires the assistant to avoid launch approval claims and state that nothing was sent.

| Attempt | Host contract | Observed result |
|---|---|---|
| Qwen3-0.6B smoke | One plain JSON action per turn; two-turn cap | Markdown-fenced output with an invented date; rejected before any call |
| Qwen3-4B initial | Same single-action prompt; eight-turn cap | Four relevant but concatenated JSON objects; rejected before any call |
| Qwen3-4B revised host | One action or an explicit array of up to four; eight-turn cap | Four requested calls executed, followed by an explanation with unsupported or omitted claims |

The first two raw outputs were not repaired or replayed as successful calls. The third is a fresh generation under a changed system prompt. All three attempts are retained. The different turn caps did not affect the first two outcomes because both stopped on their first response. This is iterative host development, not a controlled comparison of model sizes or a benchmark score.

## The final explanation still needs review

The batch attempt correctly called `check_readiness` and `draft_followup` for both platforms. Its final response described iOS as having “full compliance,” although the tool only established a scoped checklist. It claimed no evidence IDs were missing for Android, despite three unknown checks with empty evidence lists. It also failed to cite source IDs or distinguish the failed Android device check from missing evidence.

The statement that nothing was sent is supported by the tool outputs. The complete unedited response and an AI-assisted source comparison are published in the [results](../evidence/MODEL_RUNS.md). No independent human review or customer-use approval is claimed.

The existing promise-pattern lint returned **zero flags** for this response. This is a concrete example of why a narrow regex check cannot verify whether model-written claims match source evidence.

## Runtime and provenance

- Local NVIDIA GeForce RTX 5070 Ti; BF16 inference, no paid API calls or remote inference.
- Existing cached model snapshots; no model weights included in the repository.
- Worker: Python 3.10.18, PyTorch 2.8.0+cu128, Transformers 4.55.4. The MCP host uses the separate project environment (Python 3.11+).
- Non-thinking mode; sampling enabled, seed 42, temperature 0.7, top-p 0.8, top-k 20; 768 generated-token cap per turn in v0.5 (1536 in v0.6) and 12,000 input-token cap.
- Model revisions, timestamps, initial messages, prompt hash, raw responses, token counts, generation durations, tool calls and tool results are stored in each trace. Durations are generation observations, not an end-to-end customer productivity measure.
- Sampling and GPU kernels may vary across environments. Regeneration is not guaranteed to reproduce byte-identical model text.

Model references: [Qwen3-0.6B model card](https://huggingface.co/Qwen/Qwen3-0.6B) and [Qwen3-4B model card](https://huggingface.co/Qwen/Qwen3-4B). The implementation uses their documented Transformers loading and `enable_thinking=False` chat-template option. The recorded revisions, rather than a moving `main`, identify these attempts.

## Reproduce a local attempt

Install the CSM project in its usual environment. Separately prepare a CUDA-capable Python environment with the recorded PyTorch and Transformers versions and a complete local model snapshot. The model worker can use a different Python executable from the MCP host; it does not import the project package.

```sh
python scripts/run_local_host.py \
  --model-python /path/to/gpu-environment/python \
  --model-path /path/to/Qwen3-4B/snapshot \
  --model-id Qwen/Qwen3-4B \
  --revision 1cfa9a7208912126459214e8b04321603b3df60c \
  --protocol batch \
  --output work/my-local-run.json
```

PowerShell users can put the command on one line and use their Windows executable paths. Use `--protocol single` for the original host contract; add `--max-steps 2` for the small-model smoke configuration. Qwen3-0.6B used revision `c1899de289a04d12100db370d81485cdf75e47ca`.

The worker loads local files only, disables Hugging Face network access, and does not execute custom model code. It cannot download a missing snapshot. The host refuses to overwrite an existing trace. Each accepted batch is validated before any of its calls execute; unknown tool names, duplicate JSON keys, non-JSON constants and mixed final/action batches are rejected. Model-provided arguments still pass through the MCP tool schemas and engine checks. The host is scoped to this project's read-only server; it is not a general sandbox for arbitrary servers.

## Review and publishing

`python scripts/build_model_replay.py` packages the checked-in traces and review annotations into the website. It does not perform inference. CI checks structural coverage consistency, regenerates the replay and compares the artifact with Git; it does not certify the review annotations as independent truth or rerun a GPU model.

Since v0.26, the browser also renders the existing trace as a turn-by-turn conversation. It distinguishes parsed model proposals, recorded tool calls and errors, parser rejection, structured-field checks, and host correction requests. A model proposal is not counted as an executed call. Correction feedback is labeled as host-supplied assistance, including when it provides expected values. Final prose remains unverified even after fields match. The view retains initial messages, unedited model output and the full raw steps; no historical file is rewritten.

Browser-logic tests cover all eighteen recordings, the four-call unsupported answer, parser rejection with no execution, host state and decoding schemas, seven successful calls ending in a host error without final prose, distinct dependency-rejection and result-failure displays, a tool error beside successful calls, field-review corrections and escaped data. These are presentation and provenance checks, not model-quality scores. Dependency rejection and result-failure display tests use constructed cases; the policy-enabled model recording stops earlier, at parsing.

The automated coverage check asks whether the task-specific requested actions occurred: four for platform follow-ups, two for the callback handoff, two exact-message triage calls for inbound scope review, and seven fixed-fixture calls for morning review. Coverage does not check dependency order or prove that IDs were discovered from tool results; inspect the sequence separately. The separate source review examines final prose when present. Do not combine these into one unqualified accuracy number.

For an interview exercise, hide the review panel, annotate every claim in the unedited response, then compare your findings. Explain why the model can choose the correct tools yet still overstate their results, and why a zero-flag lint result should not approve the answer.

## v0.6: from parseable JSON to matching fields

Three further recordings use a structured final contract. The first returned malformed JSON after the four tool calls. The second repeated that malformed output through two correction requests. The third used optional schema-constrained generation: its parseable finals initially failed source and platform-scope checks, then matched the tool results after two corrections.

The last explanation still omits inline source IDs and the explicit nothing-sent sentence requested in the task. Structured fields and the separately rendered summary retain those facts; the prose is not approved. See [the contract and review boundaries](RESPONSE_REVIEW.md).

To reproduce the constrained configuration, install `lm-format-enforcer==0.11.3` in the model worker environment and add `--protocol grounded --max-new-tokens 1536 --repair-attempts 2 --constrain-final` to the command above. The schema controls structure; the field reviewer checks values. The recorded correction feedback contains expected values, so the final match is assisted recovery on a single task, not a held-out score or fair comparison with the earlier configurations.

## v0.9: a separate callback handoff task

The seventh recording asks for Harbor Studio's account context and a handoff for `issue_callback`, followed by a short explanation of the observation, unconfirmed hypothesis, missing fields, owner and next action. Run it with `--task callback_handoff --protocol batch --max-steps 4 --max-new-tokens 768`. The recorded attempt used no correction requests and the same cached Qwen3-4B revision as before. The grounded platform-response schema does not apply to this task; the CLI rejects that combination.

The model completed both requested actions and added a portfolio lookup and a triage call. The triage call passed the issue identifier as free-text input, rather than the customer's message. Its final answer preserved HTTP 405, Japan, both missing fields and the issue evidence ID, but described the recorded failed callback check as unconfirmed, omitted the proposed owner and endpoint-method hypothesis, and did not explicitly state that nothing was sent. It did state that no ticket was submitted.

This gives a second failure mode to inspect: valid tool arguments can still be semantically inappropriate. The two-action coverage count measures the required calls, not the quality of the extra calls or final explanation. The new task was authored during development and has not been independently reviewed. [Raw recording](../evidence/model-runs/qwen4-callback-handoff.json) and [AI-assisted comparison](../evidence/MODEL_RUNS.md).

## v0.9.1: reject a known identifier used as customer text

The server now rejects text that, after trimming whitespace, exactly equals a known issue ID. Its error directs the caller to retrieve the message or use the recorded-issue handoff tool. This is a narrow check: it does not detect arbitrary identifiers, establish the meaning of prose, or fix lexical triage's known limitations. Customer prose that includes an identifier remains accepted.

One fresh run repeated the same initial four-call batch. The extra triage call now returned an error; the model did not retry it. Both required calls succeeded. The final answer preserved the failed callback check separately from the unconfirmed cause and explicitly stated that nothing was sent, but omitted source evidence IDs, the proposed owner and the specific endpoint-method hypothesis. The unedited result remains labeled incomplete.

The run used `--task callback_handoff --protocol batch --max-steps 4 --max-new-tokens 768`, without host correction requests. Its trace records project version 0.9.1. The tool description and error behavior differ from the preceding run, so this is an observed development iteration, not a controlled improvement estimate. Older traces retain their historical tool results, including the formerly accepted identifier. Replaying an old action against the current server can intentionally produce a different result. [New raw trace](../evidence/model-runs/qwen4-callback-input-guard.json).

## v0.11: two inbound messages with no account identity

The ninth attempt asks the model to triage an annual-plan blanket-invoice request and a blank Android Offerwall message separately. Neither has a supplied account or integration ID. The task asks for one next action and two customer clarification prompts per message, the tool's route, a distinction between candidate and diagnosis, and a nothing-sent statement.

Run this task with `--task triage_scope --protocol batch --max-steps 4 --max-new-tokens 768`. It uses the same cached Qwen3-4B revision and local runtime as the callback recordings, without schema-constrained generation or host correction requests. The invoice wording reuses a published development probe. It is not held out, and there was no paired model run against the earlier engine.

**Observed:** one batch contains two calls with exact original text and `integration_id=null`. The tool returns `unknown / clarify_scope` for the invoice and `no_offers / collect_evidence` for the blank Offerwall. The model then provides a final answer. There are no extra calls, tool errors or corrections. The coverage check requires both messages and no assigned integration; two calls on the same message do not satisfy it.

**Answer review:** the response gives different next actions, two prompts per message and an explicit nothing-sent sentence. It does not invent IDs or a confirmed internal owner. The invoice prompts ask for an app/platform and expected versus actual behavior, following the tool's generic unknown-scope fallback but offering limited help with the invoice request. The phrase potential issues is tentative; the answer could more clearly distinguish lexical candidates from a confirmed diagnosis. Its actions reflect the two routes without quoting the route codes.

That customer-fit assessment is AI-assisted editorial review, not independent validation. A result can follow tool output and still ask a poorly matched question. [Unedited recording](../evidence/model-runs/qwen4-triage-scope.json) · [Published review](../evidence/MODEL_RUNS.md).

## v0.11.1: neutral questions for an unknown request

The tenth recording repeats that exact task after changing the tool's unknown-scope fallback. The old question assumed something happened to an app or platform. The new questions ask which account/product the request concerns and what information or outcome is needed. Unknown handoffs also ask the CSM to establish that scope before choosing an owner. This introduces no invoice category or billing procedure.

| Inspectable comparison | Earlier recording | Neutral-question recording |
|---|---|---|
| Project version | 0.11.0 | 0.11.1 |
| Initial prompt, task and recorded runtime settings | Same | Same |
| Initial action batch | Two exact-message triage calls, no integration identity | Same |
| Invoice route | `clarify_scope` | Same |
| Invoice tool questions | App/platform and expected versus actual behavior | Account/product context and requested information/outcome |
| Entire Offerwall tool result | `no_offers / collect_evidence` | Identical |
| Final invoice follow-up | Asks about an app/platform | Repeats the neutral account/product questions |
| Extra calls, tool errors, host corrections | None | None |

The final answer uses candidate language and explicitly says nothing was sent. Its invoice questions remain broad, and it does not explain lexical retrieval or cite the Offerwall URL. One matched development pair supports this observation, not a general quality estimate. A regression check compares the controls and verifies that the only returned-data difference is the unknown candidate's question list. It does not score the usefulness of the answer.

[Earlier raw trace](../evidence/model-runs/qwen4-triage-scope.json) · [New raw trace](../evidence/model-runs/qwen4-triage-neutral-questions.json) · [Integrity checks](../tests/test_recorded_model_runs.py)

## Queue-first morning review: first recorded attempt

The eleventh attempt starts before account selection. Its task asks for the fixed snapshot's non-live accounts strictly more than three days since contact, including unknown history, then the first account under the tool's planned-launch ordering. It requests context, readiness and English follow-ups for each integration, handoffs for recorded issues, and an evidence-citing explanation. The task contains no account, integration or issue IDs. The same batch system instruction supplies the available tool schemas.

The host task and coverage definitions were committed in `9341d2f5544bd0e9aedfe1e8d80fe763b02fe7a6` before the run. Use the reproduction command above with `--task morning_review --protocol batch --max-steps 8 --max-new-tokens 768` and a fresh output path. This uses the existing cached Qwen3-4B revision, the same sampling configuration and zero repair attempts. The fixed v0.29.8 release predates this task and recording.

**Observed:** on turn one, the model returned a five-item JSON array: `list_accounts`, `get_account_context`, `check_readiness`, `draft_followup`, and `draft_ticket`. The dependent calls supplied `12345` and `67890` as identifiers before any result had been returned. Those IDs occur in neither the prompt nor the fixture. The actual rejection was **"An action batch must contain 1..4 actions"**. The host rejected the entire batch; it did not execute the otherwise relevant queue lookup, return an invalid-ID tool error, or silently salvage a subset.

The response used 97 generated tokens and did not reach the 768-token cap. No final explanation, corrections or retries followed. Coverage is **0/7**: snapshot queue, selected account context, two readiness checks, two English drafts and one issue handoff. Those expectations are tied to this fixed fixture, with a test checking its first account and scoped records. They are evaluator knowledge, not IDs supplied to the model, and this count does not evaluate sequencing or answer usefulness.

The result does not demonstrate account discovery or a completed CSM workflow. It exposes a dependency problem in the proposed plan alongside the batch-format violation. The next attempt tests an explicit instruction to wait for the queue and context results. It remains a separate development observation, not a general reliability estimate.

[Raw recording](../evidence/model-runs/qwen4-morning-review.json) · [Browser replay](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-review#model-runs). The previous ten raw recordings are unchanged. Review annotations are AI-assisted and not independent human validation.

## Queue-first dependency instruction: no observed execution improvement

The twelfth attempt repeats the exact morning task with `--sequence-dependencies`. This optional flag adds one paragraph to the system instruction: call `list_accounts` alone, wait for its result, retrieve context using the returned first account ID, then use only IDs present in preceding results and batch only independent calls. It is accepted only with `--task morning_review --protocol batch`. It changes the model's instructions, not tool availability, parser limits or runtime ID validation. Default prompts are unchanged.

The option was committed in `d6778c42470e0a1f4673167c256d32d707872945` before inference. Add the flag to the preceding reproduction command and use a different output filename. No account, integration or issue IDs are added to the prompt. The original recording remains intact.

| Recorded comparison | Original morning attempt | With dependency instruction |
|---|---|---|
| User task, available tool schemas | Same | Same |
| Model revision and runtime sampling settings | Same | Same |
| Limits | Eight turns, 768 output tokens per turn, zero corrections | Same |
| Initial system input | Batch instruction | Same instruction plus one dependency paragraph |
| First proposed actions | Five, including dependent calls before results | Same five tool names; first four proposals identical |
| Unsupported issue ID | `12345` | `11223` |
| Host stopping condition | Batch exceeds four actions | Same |
| Executed requested calls | 0/7 | 0/7 |
| Final explanation | None | None |

The newer response uses 97 generated tokens, with no token-cap hit. It does not obey the instruction to retrieve the queue alone. No queue result, account context, drafts or tool errors are returned because batch validation rejects the whole proposal. A regression comparison verifies that removing the one dependency paragraph restores the earlier system message exactly; task text, schemas, runtime settings and caps match. These checks establish recorded controls and outcomes, not the general effectiveness of prompt changes.

This pair supports a narrow conclusion: the added instruction was insufficient in this attempt. It does not prove all dependency prompts fail. A subsequent [opt-in host policy](DEPENDENCY_POLICY.md) now enforces queue/context dependencies and checks IDs against returned scope, with scripted real-MCP tests. It is enabled by the separate `--enforce-dependencies` flag and also supplies pending-action state. The thirteenth recording below uses it; the preceding twelve recordings predate that policy. The prompt-only `--sequence-dependencies` flag does not enforce call order.

[New raw recording](../evidence/model-runs/qwen4-morning-sequenced.json) · [Replay with dependency instruction](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-sequenced#model-runs). All eleven earlier raw traces remain unchanged. This new source and recording also postdate the fixed v0.29.8 release.

## Policy-enabled attempt: parser stops the proposal first

The thirteenth attempt uses the host implementation committed in `f0cb1e428ec09cd6b595f2ecb4766fecb72db85a`. Run the same morning-review command with `--enforce-dependencies`, without `--sequence-dependencies`, and a fresh output filename. Model revision, runtime settings, user task, initial system message and schemas, eight-turn limit, 768-token cap and zero correction budget match the original morning recording.

There are two changes relative to that original attempt: the runtime dependency policy is enabled, and the host appends its current pending-action state before each generation. This is explicit planning assistance, not an isolated test of enforcement with identical model input. At the first turn it supplies one action: `list_accounts(stale_days=3, as_of=null, include_live=false)`. No account, integration or issue ID is available yet.

**Observed:** the model returns five actions, beginning with that queue call but continuing with context, readiness, follow-up and handoff calls. It supplies `account_12345`, `integration_67890` and `issue_12345` without any preceding result. The actual stopping condition remains **"An action batch must contain 1..4 actions"**. Parsing happens before dependency validation, so this trace has a `parse_error`, no `policy_error`, and no executed calls. Do not describe it as a runtime rejection of the invented IDs by the dependency policy.

| Recorded outcome | Value |
|---|---|
| Input / output tokens | 1,339 / 110; no output-cap hit |
| Executed requested calls | 0/7 |
| Policy stage before and after | `awaiting_queue` |
| Pending / completed actions | 1 / 0 |
| Selected account / final response | Neither |
| Corrections / retries | None |

The initial-message fingerprint matches the original recording because `prompt_sha256` covers `initial_messages` only. It does **not** cover the additional per-turn host message. The complete raw file, its SHA-256, `steps[0].policy_message` and `policy_before` preserve that extra input; the browser displays it before the model proposal. Regression checks verify the unchanged initial controls, added state, unchanged final policy state and parser-first rejection.

This attempt shows no execution improvement from supplying pending-action state under these settings. It does not estimate a general failure rate or invalidate the separate software tests of enforcement. A future constrained-generation attempt must be labeled as additional decoding assistance and preserved separately. Successful tool use and a faithful explanation remain unproven for this morning-review model task.

[Raw recording](../evidence/model-runs/qwen4-morning-enforced.json) · [Policy-enabled replay](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-enforced#model-runs). SHA-256: `bf65fa466c0f3acd72bb43fe0e0bfbe72ad22986b07e6ff9a477f832ee2e6c84`. All twelve earlier raw traces remain unchanged. Review annotations are AI-assisted, not independent human validation; this source and recording postdate the fixed v0.29.8 release.

## Constrained morning workflow: seven calls, then a response timeout

The fourteenth attempt uses host commit `0ab07e8af6f5c213e0ebc2217b80e08fa0949e02`. Add `--constrain-actions` to the preceding command with `--enforce-dependencies`, keeping `--task morning_review --protocol batch --max-steps 8 --max-new-tokens 768` and a fresh output path. No correction attempts or hidden retries are used. The cached model revision, recorded runtime settings, original task and initial system/tool input match the preceding policy-enabled recording.

Two things change: the host asks for exactly one pending action per turn, and the worker uses a host-derived JSON schema to constrain generation. The schema supplies permitted tool/ID combinations from prior successful results. The first queue call uses an empty argument object to invoke the fixed defaults. After completed work, the host's schema permits a final string. This is strong planning and decoding assistance; it cannot be presented as unaided model orchestration or an isolated one-factor experiment.

| Returned turn | Actual action | Input tokens | Generated tokens | Recorded generation seconds |
|---|---|---:|---:|---:|
| 1 | Snapshot queue | 1,338 | 11 | 6.492 |
| 2 | Context for returned first account `acc_014` | 2,007 | 19 | 6.434 |
| 3 | Android readiness | 3,986 | 17 | 8.255 |
| 4 | iOS readiness | 5,277 | 17 | 40.244 |
| 5 | English Android follow-up | 6,588 | 21 | 59.657 |
| 6 | English iOS follow-up | 7,467 | 21 | 92.796 |
| 7 | `issue_blank` handoff | 8,069 | 15 | 141.776 |

All seven MCP calls returned without tool errors, and every returned model response reports `schema_constrained=true`. The final policy state is `complete`, with no pending actions, and fixed-fixture coverage is **7/7**. Android remains blocked with three unknown checks and a recorded failed device check; iOS remains `checklist_complete` with a launch-plan-review draft. The handoff remains `needs_information`, missing SDK version, observation time window and redacted logs. These drafts and findings are deterministic tool outputs; the model selected permitted calls rather than composing the customer drafts.

**The answer is incomplete.** The process exited with code 1 while waiting for the next worker response. The raw trace stores `status=host_error`, `error_type=ExceptionGroup` and `final=null`. Captured stderr identifies the nested `TimeoutError` at `readline(worker, 180)`. A separate [agent-authored terminal observation](../evidence/host-observations/qwen4-morning-constrained.json) records that detail and binds it to the raw trace's SHA-256. The raw file has not been augmented with a reconstructed response or error message.

This host version persists a step only after receiving a worker response. Consequently, the eighth in-flight request and any partial model output are not in the saved trace. The seven returned schemas and results are inspectable; there is no final wording to assess for citations, selection rationale, word limit or unsupported promises. The observed latency increases alongside input length, but this single run does not establish a causal performance diagnosis or controlled benchmark.

Regression checks reconstruct the policy from the recorded results, verify each saved schema against that state, validate each model action, and compare every tool return with the current unchanged engine. They also check the separately recorded terminal observation's trace hash. These establish provenance and software consistency, not general model quality or independent human validation.

[Raw recording](../evidence/model-runs/qwen4-morning-constrained.json) · [Constrained-workflow replay](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-constrained#model-runs). SHA-256: `6f87257d6c6eda7fdc7bf836f6f435a98d086dc0d163d813563a703d9e662b97`. All thirteen earlier raw traces remain unchanged. This source and recording postdate the fixed v0.29.8 bundle. The subsequent host change below preserves in-flight inputs and specific failure causes for future runs; it does not recover this attempt's missing request.

## Preserve a request before waiting for its response

The later [optional morning final-answer mode](MORNING_FINAL.md) addresses the evidence-state distinction in the fifteenth answer. The sixteenth recording below exercises it and is rejected for an issue-only readiness citation; all fifteen earlier attempts retain their original contracts and results.

The subsequent [optional final-context reduction](MORNING_FINAL.md#optional-final-context-reduction) omits earlier host policy messages only after tool completion, retaining every tool result, current instruction and a reconstructable omission record. The seventeenth recording below uses it and returns sooner in this observed pair, while retaining the same citation mismatch. The sixteen earlier attempts retain their original inputs and outcomes.

The current host writes trace schema version 2. Before dispatch, it saves a detached copy of the full worker request (messages and any generation schema), the SHA-256 of the UTF-8 JSON plus trailing LF actually prepared for dispatch, and a `prepared` state. After writing and draining the pipe it saves `sent`. This confirms a pipe write, not model acknowledgment. Each snapshot uses a unique temporary file in the destination directory and an atomic replacement; a failed replacement leaves the prior readable snapshot. This is not a guarantee against power loss or every process-start failure.

Successful replies become `response_received`. A timeout records `response_timeout`, a direct `TimeoutError`, the configured budget and the outstanding request. EOF, invalid JSON or invalid UTF-8 becomes `worker_response_error` with its cause. Invalid JSON retains the complete rejected envelope line when available; no partial timeout output is recovered. Dispatch failures retain `host_error`, their phase and nested leaf causes. Cancellation remains `cancelled`. The host stops and cleans up the worker; it does not treat these failures as a correction request or silently retry a possibly unfinished generation.

Use `--response-timeout-seconds 300` to explicitly allow up to 300 seconds per response. The default remains **180 seconds**, the CLI accepts integers from 1 to 600, and the worker startup budget stays 180 seconds. The chosen response budget is recorded at run and request level. Changing it changes the experiment conditions; it does not demonstrate that the earlier timeout is fixed. Response timeouts, worker-response errors and worker-reported model errors exit with code 1. Existing output paths are still rejected before launch.

The replay renderer can show saved requests, failure causes and absent responses without labeling them as model proposals. The fourteen historical recordings remain byte-for-byte unchanged and have no new request fields retroactively inserted. The lifecycle changes were first checked with scripted workers through the real MCP server, including a timeout after seven calls. The subsequent actual model recording below uses this trace format. See `test_request_lifecycle_survives_worker_failures` in [the integration checks](../tests/test_host_dependency_integration.py).

## Longer response budget: a returned answer with reasoning gaps

The fifteenth recording uses host source `d5c9f289203da935a3250cd9a125475b4c070f8b` and the same constrained morning-review command with `--response-timeout-seconds 600`. Its model revision, recorded runtime settings, initial messages, task, tool schemas, eight-turn cap and zero-correction budget match the preceding attempt. The new host also persists requests and failure causes. The seven actions and returned tool results match the earlier constrained run exactly; timing is not controlled, so this is not a speed benchmark or an estimate of general reliability.

**Observed:** all seven calls complete, then the eighth turn returns an 80-word final explanation. The process exits 0 with `status=final_response`, and the policy is complete. The final generation takes **272.986 seconds**, exceeding the previous 180-second cutoff but staying within this run's explicit budget. No correction, retry or output-cap hit occurs. Every request includes its complete messages, decoder schema, byte fingerprint and lifecycle timestamps.

| Turn | Action | Input tokens | Generated tokens | Generation seconds |
|---|---|---:|---:|---:|
| 1 | Snapshot queue | 1,338 | 11 | 4.755 |
| 2 | Returned-account context | 2,007 | 19 | 4.763 |
| 3 | Android readiness | 3,986 | 17 | 6.444 |
| 4 | iOS readiness | 5,277 | 17 | 34.662 |
| 5 | English Android follow-up | 6,588 | 21 | 48.105 |
| 6 | English iOS follow-up | 7,467 | 21 | 80.211 |
| 7 | Recorded-issue handoff | 8,069 | 15 | 102.349 |
| 8 | Final explanation | 9,018 | 134 | 272.986 |

The unedited answer and an AI-assisted claim review are available in the [replay](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-long-budget#model-runs). Its strengths and gaps are distinct:

- Account name, planned October 16 launch, non-live state, five-day contact age and iOS `checklist_complete` match the returned records. It does not explicitly explain the first-account ordering relative to the other queued accounts.
- The phrase **"missing currency approval and device verification"** merges `currency_approved=unknown` with `device_verified=not_met`. The latter has a cited failed test record; it is not missing evidence. The wording does not preserve the task's required distinction.
- **"SDK version, time window, and redacted logs"** correctly lists all three missing handoff fields. The underlying draft remains `needs_information`, `root_cause=unconfirmed` and `sent=false`.
- It names two real evidence IDs, but omits the available contact and iOS sources. It describes platform states without explicitly contrasting the Android evidence request with the iOS launch-plan review.
- It says **"No evidence was sent or submitted."** The trace independently records unsent drafts. The answer makes no launch-approval, issue-resolution or confirmed-root-cause claim. Its 80 whitespace-separated words are within the requested 220-word limit; length is a mechanical check, not a fidelity score.

The browser pairs the problematic state wording and the correct handoff list with exact historical fields. Comparison generation requires matching excerpts, unambiguous scoped calls and checks, successful results and one authored review per excerpt. Request-history checks reconstruct each message sequence and fingerprint, validate the saved schemas against policy state, and compare all tool outputs with the unchanged engine. These are provenance and software checks; the prose assessment remains AI-assisted, not independent human validation.

[Raw trace](../evidence/model-runs/qwen4-morning-long-budget.json), SHA-256 `aead6eaa015718e276ded9ff568281d5e418b8aadbb01fb10cfd749b6c1fc3e6`. All fourteen earlier raw recordings remain unchanged. The fixed v0.29.8 package predates this recording. The next substantive gap is faithful explanation of evidence states and next actions, not obtaining another syntactically valid final string.

## Morning field review: a real citation with the wrong purpose

The sixteenth attempt uses host source `a982c15ed6fd23e5bbb480ca8628afbca9d71e03` with `--review-morning-final`, constrained actions, eight turns, a 600-second response budget and zero corrections. The output cap changes from 768 to 1536. All other recorded runtime settings, the task, initial instructions and all seven tool-stage worker requests match the prior longer-budget run. Actions and tool returns also match exactly. The final request adds the system-role [contract](MORNING_FINAL.md) and a structure-only schema. These changes are disclosed assistance; this single development attempt is not a causal accuracy or speed comparison.

**Observed:** seven successful calls, followed by a schema-valid structured answer. The final generation takes **405.461 seconds**, with **9,386 input tokens** and **314 generated tokens**. No token cap, retry or correction occurs. Field review reports exactly one mismatch and the host exits 1 with `status=rejected`. It is a returned answer rejected on values, not a timeout or parsing failure.

| Component | Recorded outcome |
|---|---|
| Account selection fields | Match the first returned account, timing and contact citation |
| Android checks | Three unknown checks and the failed device check remain separate |
| iOS checks | Checklist complete with no unknown/failed checks; no launch approval |
| Follow-up purposes | Android evidence request; iOS launch-plan review |
| Handoff fields | Correct scope, three missing fields, issue citation and unconfirmed cause |
| Readiness citations | Android adds `msg_issue_blank` to the three actual readiness sources; rejected |
| Checked summary | Withheld (`null`) because a field mismatch remains |
| Free prose | 46 words; not semantically verified by the host |

The extra citation is not fabricated or borrowed from another platform. It identifies the original customer report on the same Android issue and correctly belongs in the handoff's evidence list. It is not among the readiness checks' source IDs. This makes the failure useful to explain: **a real, correctly scoped source still needs to support the particular claim being made.**

The model's explanation preserves unknown versus failed checks and says nothing was sent. It does not explain why this account comes first under planned-launch ordering, state the different platform next actions, name the missing handoff fields or cite evidence IDs. Those fields are available elsewhere in the JSON; their presence does not make the prose a complete response. This assessment is AI-assisted comparison with the returned records, not independent human validation.

[Inspect the replay](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-field-review#model-runs) and [raw trace](../evidence/model-runs/qwen4-morning-field-review.json). SHA-256: `e3dd594b3bc257e73df11f77a34006fb440dc3f1f7e229cba9862d341ee3be6a`. The host's rejection, original payload and exact final contract remain inspectable. All fifteen earlier raw recordings are unchanged. This result and source postdate the fixed v0.29.8 bundle. No reliability rate, customer outcome or personal mastery follows from this attempt.

## Reduced final context: lower recorded latency, same field failure

The seventeenth attempt uses host source `f87b540911c5bb6e0a8c5cf9516789cfcd088c9e` and adds `--compact-final-context` to the preceding field-review configuration. Model revision, recorded runtime settings, task, initial instructions, final contract, decoder schema, eight-turn cap, 600-second response budget and zero-correction budget match. All seven tool-stage requests, model proposals and returned tool results match exactly.

The final request keeps **18 of 25 messages**, omitting seven superseded host policy messages by their recorded positions. Every tool result remains unchanged. Recombining the retained input with its omission audit reconstructs the preceding run's complete 25-message history exactly. The actual worker request and its byte fingerprint are saved separately from the audit.

| Observed final turn | Full policy history | Reduced policy history |
|---|---:|---:|
| Messages sent | 25 | 18 |
| Input tokens | 9,386 | 7,728 |
| Generated tokens | 314 | 322 |
| Generation seconds | 405.461 | 94.323 |
| Structured-field review | Rejected | Rejected |
| Explanation words | 46 | 52 |
| Correction attempts | 0 | 0 |

These are final-generation measurements, not total workflow times. The recorded response is faster in this pair, but hardware load and timing were not controlled and generated wording differs. This is one exploratory comparison on an already inspected synthetic task, not a general speedup estimate, causal performance result or production guarantee.

Every structured final field except `explanation` is identical to the preceding run. Android again includes `msg_issue_blank` among readiness citations. The reviewer reproduces the same single `lantern_android.evidence_ids` mismatch, withholds the checked summary and leaves prose verification unperformed. The process exits 1 with `status=rejected`; no correction, retry or output-cap hit occurs.

The 52-word explanation names Lantern Games, preserves unknown versus failed checks and says nothing was sent or submitted. It still does not explain the contact threshold and first-account ordering, specify platform-specific next actions, list the missing handoff fields or cite evidence IDs. Correct fields elsewhere in the JSON do not fill those gaps in the prose. This is AI-assisted source comparison, not independent human evaluation.

[Open the reduced-context replay](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-compact-context#model-runs), [compare the prior run](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-field-review#model-runs), or inspect the [raw trace](../evidence/model-runs/qwen4-morning-compact-context.json). SHA-256: `d22d9e66343c50b265720a358a1ae2ab62b26bbe154899d90c8b26ffecd967d6`. All sixteen earlier raw traces remain unchanged. This recording postdates the fixed v0.29.8 bundle. It demonstrates why input reduction, latency, field correctness and explanation usefulness should be assessed separately.


## One correction: matching fields, unchanged explanation

The eighteenth attempt uses host source `5412145c0f5207a3ab0bae3cdcf7e72315c28ac2`. It keeps the preceding reduced-context configuration and allows **one correction** with a **nine-turn cap**. Model revision, recorded runtime settings, task, initial instructions, final contract, decoder schema and 600-second response budget match. The first eight worker requests and model response texts are identical to the seventeenth recording, including the rejected final answer; all seven tool results match exactly. Hardware load and timing are not controlled.

The host supplies the expected readiness citation list after the same `lantern_android.evidence_ids` mismatch. Turn 9 removes `msg_issue_blank` from Android readiness evidence while keeping it in the handoff. **Every other field, including the 52-word explanation, is unchanged.** The host exits 0 with `status=structured_fields_match`, no review issues and a separate system-rendered summary. This is recovery with supplied expected values on an inspected task, not independent self-correction or a reliability estimate.

| Recorded final response | Initial answer | After one correction |
|---|---:|---:|
| Turn | 8 | 9 |
| Input tokens | 7,728 | 8,540 |
| Generated tokens | 322 | 318 |
| Generation seconds | 86.177 | 264.883 |
| Field review | Rejected | Structured fields match |
| Explanation words | 52 | 52, identical text |

The correction request retains 21 of 29 messages. It includes all tool results, the rejected answer, both final-contract messages and the explicit correction feedback; eight superseded policy messages are recorded in the omission audit. The saved requests and hashes permit exact reconstruction. No tool call is repeated and neither final generation hits the output cap. These are observed response measurements, not total workflow time or a general latency comparison.

The explanation still omits the contact-threshold and first-account ordering rationale, the distinct platform next actions, the three missing handoff fields and source IDs. It preserves unknown versus failed checks and the nothing-sent statement. The host explicitly leaves `free_text_verification=not_performed`; the system-rendered summary supplies checked tool facts separately. This prose assessment is AI-assisted rather than independent human review.

Reproduction uses the same cached model and local worker environment described above, a fresh output path, and these arguments:

```sh
python scripts/run_local_host.py --model-python <local-model-python> --model-path <cached-Qwen3-4B-snapshot> --model-id Qwen/Qwen3-4B --revision 1cfa9a7208912126459214e8b04321603b3df60c --task morning_review --protocol batch --enforce-dependencies --constrain-actions --review-morning-final --compact-final-context --response-timeout-seconds 600 --max-steps 9 --max-new-tokens 1536 --repair-attempts 1 --output <new-trace-path>
```

[Open the correction replay](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-correction#model-runs), [inspect the raw trace](../evidence/model-runs/qwen4-morning-correction.json), or review the [recording audit](../tests/test_morning_correction_recording.py). SHA-256: `30e84bfb72ba5b9918a74c64137403c421149889119179da82cb284e07347e50`. All seventeen earlier raw traces and their review entries remain unchanged. This recording postdates the fixed v0.30.1 package. It adds a concrete example of a repaired structured claim alongside an unchanged, incomplete explanation; no customer outcome or personal mastery is inferred.


## Next configuration: an explicit explanation checklist

The [optional explanation checklist](MORNING_FINAL.md#optional-explanation-checklist) targets the omissions retained by the eighteenth attempt. Add `--explanation-checklist` to its command with a fresh output path. It appends fixture-independent writing guidance only after tool completion, before the unchanged final contract. The schema, field checker, task and model settings need not change.

This is a prepared, software-tested configuration; the eighteen published recordings predate it. A future result must be compared against the preserved one-correction baseline, with the new guidance disclosed as assistance. Inspect selection rationale, distinct platform next actions, missing handoff fields, source citations, unknown-versus-failed distinctions and boundary statements separately. Retain failures and unchanged wording rather than calling a field match an explanation-quality improvement.
