# Check morning-answer fields before presenting the explanation

The [fifteenth recording](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-long-budget#model-runs) completes seven calls and returns an answer, but describes unknown currency approval and a recorded failed device check together as missing verification. Its final schema only requires a nonempty string. This optional host extension asks for explicit fields and checks them against the returned workflow before producing a separate summary.

**Current evidence:** authored counterexamples, decoder-parser checks, scripted workers through the real MCP server and two actual model attempts: the [original field-review run](LOCAL_MODEL.md#morning-field-review-a-real-citation-with-the-wrong-purpose) and the [reduced-context run](LOCAL_MODEL.md#reduced-final-context-lower-recorded-latency-same-field-failure). Both return schema-valid answers with the correct unknown/failed distinction, but the reviewer rejects the same issue-only readiness citation. No correction occurs and no checked summary is issued. All fifteen earlier recordings retain their original contracts and outcomes. These two development attempts do not establish reliable generation or faithful prose.

## The contract

| Answer component | Required agreement with recorded results |
|---|---|
| Selection | First returned queue account; contact state, contact age, days to planned launch and its context's contact source IDs |
| Each selected integration | Readiness decision; all `unknown` checks separately from all `not_met` checks; exact union of readiness source IDs; English draft's follow-up purpose |
| Each recorded issue | Integration scope, complete missing-field list, issue source IDs, handoff state and unconfirmed root-cause state |
| Boundaries | `nothing_sent=true`, `launch_approved=false`; recorded drafts remain unsent |
| Explanation length | 1–220 whitespace-separated words; no semantic approval |

Every selected integration and issue must appear exactly once. List order is immaterial, but duplicate and extra entries are rejected. IDs come from the observed queue/context, not Lantern's known answers. An empty queue requires `selection=null` and empty platform/handoff lists. Unknown numeric contact history remains null, not zero.

The reviewer replays the dependency policy from recorded calls. Missing work, wrong scope, duplicated successful calls and unresolved tool errors cannot support a passing review. A failed call can be retried while it remains pending. The reviewer also requires unambiguous context sources, correctly scoped references, complete readiness-check IDs and valid draft-purpose/intake fields. Matching those fields does not independently verify the records' truth or freshness.

## Where assistance enters

Enable `--review-morning-final` with `--enforce-dependencies`, which already requires `--task morning_review --protocol batch`. Existing default behavior is unchanged. The host appends a `final_contract_message` only after no work remains pending. It uses the system role to explicitly replace the earlier final-string format; the cached Qwen3 chat template accepts later system messages. Scripted integration checks confirm that the preceding seven worker requests match the existing constrained workflow exactly.

The added message names the fields and explains their meanings, using placeholders rather than fixture answers. Its full text and request fingerprint are saved. With `--constrain-actions`, the decoder receives a new final-object schema containing types and state vocabularies, but no fixture IDs or expected readiness answers. A schema-valid response can still misclassify a failed check; the separate result-based review rejects it. Without constrained decoding, the same message and review apply but generation is unconstrained.

Invalid final payloads remain inspectable. The host records `response_review` on the turn and trace, and exits 1 for a rejected final in this mode. No silent repair occurs. An explicitly enabled correction budget uses the existing feedback mechanism; feedback may supply expected values and is recorded as host assistance. `structured_fields_match` is a narrow field result, not approval for customer use.

The recorded experiment uses this configuration; choose a fresh output path when reproducing it:

```sh
python scripts/run_local_host.py \
  --model-python /path/to/local-model-python \
  --model-path /path/to/cached-model \
  --model-id Qwen/Qwen3-4B --revision YOUR_CACHED_REVISION \
  --task morning_review --protocol batch \
  --enforce-dependencies --constrain-actions --review-morning-final \
  --response-timeout-seconds 600 --max-steps 8 --max-new-tokens 1536 \
  --repair-attempts 0 --output new-morning-field-review.json
```

The recorded result is a rejected final answer, not a passing field review. The larger output cap explicitly changes the preceding run's 768-token condition; it is not a measured optimum, and the returned 314-token response does not reach either cap. Timeouts and incomplete JSON must also remain visible in future attempts. See [local model setup and provenance](LOCAL_MODEL.md) for the optional environment and decoder dependency.

## Optional final context reduction

The sixteenth attempt's final generation took 405.461 seconds. The optional `--compact-final-context` flag prepares a narrower final input. It requires `--review-morning-final` and applies only after all tool work is complete. The seventeenth recording uses the reduction: final input falls to 7,728 tokens and final generation takes 94.323 seconds, while the same citation mismatch remains. Existing defaults and all sixteen earlier recordings are unchanged. This single observed pair is not a general latency benchmark.

The host records the position of each workflow-policy message when it creates that message. For a final request, it omits earlier policy messages and retains the latest policy, initial instructions, task, every model response and tool-result message, final contracts and any correction feedback. Selection uses these host-owned positions rather than matching customer text. The canonical conversation remains intact; a later correction builds its request from that full history again.

Each reduced request saves `context_reduction`: the method, original and retained message counts, retained positions, and every omitted message with its original position. Combining that audit with the exact saved worker request reconstructs the complete pre-reduction history. Request fingerprints continue to cover the bytes actually sent. The browser exposes the reduction separately from the model's proposal. This omission record is retained even when the worker times out before answering.

An authored check replays the sixteenth recording's final input through this helper: **18 of 25 messages remain**, with seven superseded policy messages omitted and every tool result unchanged. This is a mechanical transformation of a saved request, not new inference or a measured speedup. Scripted real-MCP tests cover a matched answer, a rejected answer followed by explicitly budgeted correction, and a final-response timeout. The same field checker and prose-review boundary still apply.

Add `--compact-final-context` to the command above for a new experiment with a fresh output path. Compare recorded input tokens, generation time, field review and explanation quality; a shorter input alone establishes none of the latter outcomes. See [the helper](../src/csm_copilot/host_context.py), [preservation checks](../tests/test_host_context.py) and [integration checks](../tests/test_host_dependency_integration.py).

## Recorded correction after the citation rejection

The [eighteenth attempt](LOCAL_MODEL.md#one-correction-matching-fields-unchanged-explanation) permits one correction and a ninth turn. Its first eight requests and response texts reproduce the reduced-context attempt exactly. The host supplies the expected readiness source list; the model removes the extra issue citation, retains its handoff use and matches the checked fields. The explanation remains identical. The saved ninth request includes the rejected answer, feedback and every tool result, with its own context-omission audit. This is an observed recovery with expected-value assistance, not independent self-correction.

## Optional explanation checklist

`--explanation-checklist` requires `--review-morning-final` and defaults off. It adds a separate system-role writing checklist immediately before each final-answer contract, after the dependency policy reports that tool work is complete. The tool-stage inputs and existing structured schema remain unchanged.

The checklist asks the model to explain queue qualification and ordering, propose a concrete next action for each platform, distinguish unknown evidence from recorded failures, name missing handoff fields, attach appropriate source IDs, and preserve the nothing-sent and no-launch-approval boundaries within 220 words. It contains no fixture account/integration/issue identifiers or expected answer values. It is additional prompt assistance, not a semantic checker or an authored replacement answer.

The trace records the top-level `explanation_checklist` setting and each `explanation_guidance_message`. Exact worker inputs and fingerprints include the message. Context reduction retains it, including earlier copies and correction feedback, while still omitting only superseded policy messages. The browser identifies the checklist separately as host assistance. Older recordings without the setting display **Not recorded**, rather than an inferred disabled value.

Scripted workers through real MCP verify final-only insertion, unchanged tool-stage requests, complete request reconstruction, full and reduced context, unconstrained actions, correction and timeout retention. A scripted answer with matching fields and an unsupported launch/revenue claim still matches the field checker with `free_text_verification=not_performed`; adding guidance does not certify the prose. These are software tests. None of the eighteen published model recordings uses this option yet, so no improvement in model explanation quality is claimed.

For the next local experiment, add `--explanation-checklist` to the [one-correction configuration](LOCAL_MODEL.md#one-correction-matching-fields-unchanged-explanation) and choose a new output path. Keep the baseline, exact guidance, first answer, any feedback and final answer. Review whether the requested information is actually present and supported; a longer explanation or a matching field report alone is insufficient.

## Checked summary versus model prose

On agreement, the host renders a separate summary from the actual queue, readiness, follow-up and handoff results. It preserves unknown versus failed checks, citations and distinct next actions. The model's own explanation remains separate, and the browser identifies the final-contract message as host assistance.

A counterexample supplies correct fields alongside "Both launches are approved and revenue is guaranteed." Field review passes, while `free_text_verification=not_performed` and `human_review_required=true` remain explicit. The unsupported sentence is absent from the system-rendered summary. This demonstrates a limit of field checking; it does not make that prose acceptable.

The checker does not verify the meaning of arbitrary draft bodies, confirm customer reports independently, assess tone or establish production performance. These optional local-host controls do not automatically apply to arbitrary MCP clients.

## Inspect and explain

Read [the reviewer](../src/csm_copilot/morning_review.py), [the counterexamples](../tests/test_morning_final.py) and [the real-MCP host checks](../tests/test_host_dependency_integration.py). Predict what happens when follow-up purposes are swapped, an issue citation is used as readiness evidence, or matching fields accompany unsupported prose. Keep your own prediction and explanation separate from the supplied expectations; these tests do not establish personal mastery.
