# An actual model run, including the failures

The project contains twelve exploratory local model attempts across four synthetic CSM tasks. Unlike the scripted MCP smoke test, a language model proposed the tool names and arguments. The host executed accepted calls through the real MCP stdio transport and returned their full results to the model. Rejected proposals are retained without being counted as executed calls.

The newest attempt repeats the morning-review request with explicit dependency guidance: retrieve the queue alone, wait for context and use IDs from earlier results. It still proposes five actions and unsupported identifiers before reading any result. The unchanged four-action batch limit rejects the entire response. Neither morning attempt demonstrates account discovery. The paired inputs and outputs are preserved below.

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

Seven browser-logic tests cover all twelve recordings, the four-call unsupported answer, parser rejection with no execution (including both queue-first attempts), a tool error beside successful calls, two field-review corrections, exhausted parse corrections, and escaping model/host/tool text. These are presentation and provenance checks, not model-quality scores.

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

This pair supports a narrow conclusion: the added instruction was insufficient in this attempt. It does not prove all dependency prompts fail. A subsequent [opt-in host policy](DEPENDENCY_POLICY.md) now enforces queue/context dependencies and checks IDs against returned scope, with scripted real-MCP tests. It is enabled by the separate `--enforce-dependencies` flag and has no model recording yet. It also supplies pending-action state to the model. The twelve recordings predate that policy; the prompt-only `--sequence-dependencies` flag does not enforce call order.

[New raw recording](../evidence/model-runs/qwen4-morning-sequenced.json) · [Replay with dependency instruction](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-sequenced#model-runs). All eleven earlier raw traces remain unchanged. This new source and recording also postdate the fixed v0.29.8 release.
