# Check structured claims before rendering a summary

The first completed local model run called the right tools but overstated their results. Version 0.6 adds a structured final-response contract and checks it against the tool outputs actually observed in that run. The original free-text response and every subsequent attempt remain published.

## What is checked

Each requested integration must appear once. The model supplies its readiness decision, unknown check IDs, failed check IDs and readiness source IDs. The reviewer compares those fields with the latest successful `check_readiness` output for that integration. It also requires an observed English follow-up and verifies the read-only draft state.

| Field | Review rule |
|---|---|
| Integration scope | Exactly the requested integrations; no duplicates, omissions or extras |
| Decision | Exact match to the observed scoped readiness decision |
| Unknown checks | Exact set of checks whose state is `unknown` |
| Failed checks | Exact set of checks whose state is `not_met` |
| Evidence IDs | Exact union of IDs attached to that integration's readiness checks; duplicates are rejected |
| Nothing sent | Must be true; observed follow-up results must also show no sending or contact-history change |
| Launch approved | Must be false; scoped checklist completion does not approve launch |
| Explanation | Retained unedited and explicitly **not semantically verified** |

An issue message may be relevant to a follow-up without establishing the state of a readiness check. The final contract therefore does not permit copying the follow-up's entire evidence list into the readiness evidence field. This is a source-role distinction, not a claim that the issue report is irrelevant or untrue.

## Two outputs with different meanings

When the fields match, the system renders a separate summary directly from the observed tool results. It preserves every check state, source ID and proposed next action. This text is labeled system-rendered; it is not attributed to the model.

The model's free-form explanation is displayed separately. A matching structured response does not approve that explanation. A regression test intentionally supplies matching fields alongside a false revenue guarantee and verifies that the prose remains unverified and is excluded from the system-rendered summary.

The status is `structured_fields_match`, not `approved`, `safe` or `factually_correct`. These checks establish agreement with recorded tool outputs, not the truth, freshness or completeness of the source evidence.

## Bounded correction requests

The optional local host accepts `--protocol grounded`. It can also use `--repair-attempts 0`, `1` or `2`; zero remains the default. A correction request includes the parsing error or exact field mismatches. The model must generate a new response; the host does not silently edit the raw output.

Every response, review result and correction message is retained in the trace. Once the correction budget is exhausted, rejection remains visible. The outer model-turn cap still applies. This is a controlled development workflow, not an independent evaluation: feedback gives the model the expected values already available in the tool data.

Use the same local setup described in [the model experiment](LOCAL_MODEL.md), then add:

```sh
--protocol grounded --max-new-tokens 1536 --repair-attempts 2
```

The larger output cap accommodates explicit source IDs. It is a changed configuration from the original free-text runs, so the attempts must not be presented as a controlled model-quality comparison.

The recorded unconstrained attempt returned malformed nested JSON. A fresh run with two correction requests repeated the same error. Both recordings are retained; correction prompts alone did not solve the format failure.

## Optional schema-constrained generation

The host also supports `--constrain-final`, requiring `lm-format-enforcer==0.11.3` in the local model environment. Once all requested tool actions are observed, the host supplies a final-response JSON schema to the worker. The model still generates the field values and prose, but its allowed next tokens are filtered by that schema. The schema and a per-turn constraint flag are saved in the trace.

The schema specifies types, required fields and allowed readiness/check labels. It does not contain the expected integration decisions or source IDs. Those are checked separately against the tool results. Generation can still hit its token cap or fail; the parser and field reviewer remain mandatory. Free prose is never certified by the schema.

This uses the documented Transformers prefix-token integration from [LM Format Enforcer](https://github.com/noamgat/lm-format-enforcer). The optional dependency was installed in a separate local environment sharing the existing GPU libraries; the base project does not require it and CI does not perform model inference.

## What to demonstrate

Open the recorded attempts and identify the difference between: tool execution, a parseable response, matching structured fields, and a faithful explanation. Then inspect the system-rendered summary and show exactly which source supports the Android failure and which checks remain unknown.

The test suite covers cross-platform and invented IDs, omitted failures, omitted unknowns, duplicate sources, missing tool observations, changed boundary booleans and the limit of checking free prose. The recorded model attempts provide execution evidence; neither the tests nor the AI-assisted review constitute independent human validation.

## Observed constrained result

The recorded constrained run executed four requested calls. Its first final duplicated Android entries and included the issue-only source `msg_issue_blank` in readiness evidence; its second final still duplicated platforms. The third final, after two corrections, matched the observed structured fields. All responses and feedback are preserved in [the trace](../evidence/model-runs/qwen4-constrained.json).

The final explanation still lacks inline source IDs and the explicit nothing-sent sentence requested by the task. The structured fields and separate system-rendered summary include that information. This illustrates the remaining gap between field agreement and complete instruction following, even after assisted recovery.
