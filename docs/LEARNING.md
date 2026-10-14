# Learning path: make the project yours

The project is a starting point for demonstrated understanding. These exercises are **not marked complete**. Keep personal notes and small commits as you work through them; that is stronger evidence of learning than an oversized feature list.

**A small current exercise:** compare the two [inbound-message recordings](LOCAL_MODEL.md#v0111-neutral-questions-for-an-unknown-request). Before reading the annotations, explain why a correct `unknown` category can still produce a poor invoice follow-up. Propose one more specific customer question without inventing billing policy. Then trace the changed question through the engine, tool result and unedited model response. Record your reasoning separately from the AI-assisted review.

## First run — read the decision before the full packet

After the README's installation steps, run:

```sh
csm-demo --format summary
```

The [published output](../evidence/morning-summary.txt) contains three accounts and four platforms at the fixed synthetic snapshot. Find `Moon Garden / Android: blocked` and trace `lantern_android_device_verified` back to the evidence. Contrast it with `Moon Garden / iOS: checklist_complete`. Explain why Meadow's unknown device evidence leads to a different state from a recorded failure.

Next, inspect a complete platform brief:

```sh
csm-demo --format markdown --integration lantern_android --output android-review.md
```

Compare the summary's missing handoff fields with the detailed brief. Write your explanation before reading the implementation in `src/csm_copilot/summary.py`. The summary consumes existing workflow results; it does not change the decision rule, contact history or source records. Its counterfactual updates are excluded. This is a suggested exercise, not a record of completed personal work.

## Session 1 — Trace one account (30–45 minutes)

- Find `acc_014` in `src/csm_copilot/data/accounts.json`.
- Draw its two integration records and trace one evidence ID.
- Explain why iOS has a complete checklist and Android does not.
- Run `csm-demo --output review-packet.json` and locate the same records.
- Write five sentences explaining `unknown` versus `not_met` without looking at this guide.

Evidence to keep: a short note linking the exact record and rule you explained.

## Session 2 — Change one rule input (30–45 minutes)

- In a local experiment, remove Meadow's device evidence. Predict the result before running.
- In a separate experiment, make the device check `not_met` with a valid evidence reference.
- Explain why the overall decision changes from `needs_evidence` to `blocked`.
- Find the test that prevents iOS evidence from being applied to Android.
- Revert the experiments or keep them in a clearly named test fixture.

Evidence to keep: prediction, output, explanation and a small test you can defend.

## Session 3 — Understand the MCP boundary (45 minutes)

- Read `server.py`; explain what the decorators expose.
- Run the real stdio smoke test and inspect `evidence/mcp-transcript.json`.
- Explain why tool transport success does not measure the host model's reasoning.
- Connect a model-enabled host if available and run `morning_review`.
- Record host/model/version, prompt, tool calls and final output. Redact any private environment information.

Evidence to keep: a transparent live trace labeled with its actual execution mode. Do not relabel the scripted transcript as a model run.

## Session 4 — Investigate a failure (45–60 minutes)

- Pick one negation or paraphrase failure in the evaluation.
- Explain why the lexical method fails.
- Ask a person unfamiliar with the implementation to write new cases, without showing them your keyword patterns.
- Define the expected categories before running the tool.
- Compare a proposed improvement against the current baseline using the same cases and available information.

Evidence to keep: case authorship, expected outputs, actual outputs and examples where the improvement still fails. Do not tune on the existing holdout phrases and claim a new unbiased score.

## Session 5 — Practice the customer conversation (30 minutes)

- Rewrite one template in your own English and Chinese.
- Underline every factual claim and match it to an evidence ID.
- Circle each deadline or promise and explain whether it is supported.
- Explain the issue to a nontechnical teammate in under one minute.
- Then explain the technical handoff to an engineer in under one minute.

Evidence to keep: your two versions and the claim-to-evidence annotation.

## Personal mastery checklist

Additional v0.11 exercise: select **Qwen3-4B · two inbound messages** and read its unedited answer before the review panel. Separate three judgments: were the correct tools called, does the answer follow their results, and do its questions fit the customer's request? Rewrite only the invoice questions in your own words. Do not invent billing procedures or imply that an invoice was sent. Keep your initial assessment and later reflection separate.

Additional v0.10.1 exercise: before opening the [phrase-boundary report](../evidence/TRIAGE_BOUNDARIES.md), predict the categories for `blanket invoice`, `blank invoice`, `The Offerwall keeps blanking` and `Android页面blank`. Run the tool and explain which result depends on spelling boundaries and which requires understanding the sentence. Explain why a general Unicode word-boundary expression could lose the mixed Chinese/English signal. Write down one remaining failure before proposing a broader classifier. This exercise is not recorded as completed.

Additional v0.5 exercise: inspect [the unedited local model response](LOCAL_MODEL.md) before opening the review notes. Mark supported, unsupported and omitted claims. Explain how all four requested tool calls can succeed while the final explanation remains unsuitable for use, and why the narrow promise lint returned zero flags.

Additional v0.4 exercise: work through [the Product feedback review](PRODUCT_FEEDBACK.md). Predict how counts change if a second platform from the same account has a gap. Explain why the callback denominator differs from the device-check denominator, then write a Product question without asserting an unverified cause.

- [ ] I can explain the customer problem without saying “AI automation” as a substitute.
- [ ] I can trace one output back to a source record and public documentation.
- [ ] I can explain all four readiness states and the aggregation rule.
- [ ] I can explain why a draft must not update contact history.
- [ ] I can run the tests and explain one failure.
- [ ] I can distinguish deterministic replay, scripted MCP transport and live model orchestration.
- [ ] I can explain at least two limits of the evaluation.
- [ ] I can point to one improvement I personally made and verified.

## Short reflection template

Additional v0.2 exercise: read [the evidence-scope failure and fix](EVIDENCE.md), predict the eight probe outcomes, then write a new provenance test in your own words. Explain why validating source ownership does not prove that the source is true.

```text
Date:
Question I investigated:
My prediction:
Code or record I inspected:
Observed result:
What I misunderstood:
What I changed:
How I checked it:
What remains uncertain:
```

## v0.6 demonstration exercise

Open the "Qwen3-4B · constrained JSON + field review" attempt. Explain the initial source-role error and repeated platform entries, then show the two correction requests and final matching fields. Expand the system-rendered evidence summary. Identify why it is different from the model explanation, and find the missing inline citations and nothing-sent sentence in that explanation. [Response-review design](RESPONSE_REVIEW.md).

Describe the work as an AI-assisted development experiment with inspectable failures. Personal mastery is demonstrated when you can trace a rejection to its source, predict a new failure case, and explain or implement a small change yourself; it is not established by the number of tests or iterations in the repository.

## v0.7: keep a before-and-after reflection

Use [the interactive practice](PRACTICE.md) to choose an action and explain your reasoning before revealing guidance. The download keeps that original response separate from your later reflection. These are your notes, not an automated evaluation. Complete the exercise yourself before describing it as personal learning evidence. The public site and repository contain no claimed completion by Yuchi.

## Trace a small arithmetic-to-workflow bug

Use the [queue-order regression](DEVELOPMENT.md#v0161--keep-rounded-display-values-out-of-queue-ordering) as a source-reading exercise. Two accounts launch at 09:01 and 09:02 UTC, but both display as 2.0 days away. Predict what happens if account ID breaks a tie in those displayed values. Then read `list_accounts` in `engine.py`, compare the preserved pre-change output, and run:

```sh
python -m pytest -q tests/test_queue_order.py
```

Explain why rounding is appropriate for display but loses information needed for prioritization. Describe how timezone offsets and true ties should behave. Keep your prediction separate from what you learn after reading the fix; this exercise is not marked complete for you.

## Explain why moving the clock does not refresh the records

Compare the default `list_accounts` result with the later-date call in [the scripted MCP transcript](../evidence/mcp-transcript.json). Locate `as_of`, `dataset_as_of`, `time_basis` and `records_refreshed`. Explain why the contact age changes while Lantern's recorded stage and Android readiness do not.

Predict whether `2026-10-14T05:00:00-04:00` represents the dataset snapshot or a later review. Then run `python -m pytest -q tests/test_review_time.py` and explain the timezone-equivalence check. Identify which new customer evidence would be needed before describing a changed stage or resolved issue. This is a suggested exercise, not a completed personal reflection.

## Turn generic triage questions into a focused handoff

This is also available as decision 4 in [interactive Practice](https://yuchi-wang02.github.io/csm-copilot/#practice). The exercise presents Harbor's original record and handoff gaps before guidance, then lets you save your first reasoning separately from your later reflection.

Open [Harbor's handoff](https://yuchi-wang02.github.io/csm-copilot/?case=harbor_android&view=handoff&lang=en#workspace) and expand its original issue record. Before reading the candidate questions, list what is known, what is missing and what remains a hypothesis. Then compare the suggested questions with the record: which facts would be redundant to ask for again?

Write a short customer follow-up that requests only the missing details. Trace each retained question to either a missing handoff field or a candidate check, and explain why HTTP 405 alone does not establish the cause. Download the platform brief and verify that another reviewer could find the same original report and questions. Save your own first reasoning and later revision separately; this guide does not supply or certify your personal answer.

## Distinguish a reported symptom from a test observation

In the handoff's original-record disclosure, find the source type and recorded timestamp. Explain what additional context you would want if the same symptom came from a test record instead of a customer report. A label identifies the declared origin; it does not prove reproducibility or current customer impact.

Inspect `test_export_identifies_issue_source_kind_and_uses_the_original_record` in `tests/test_case_brief.py`. Predict which wording should appear when a copied handoff field disagrees with the original source, then run that focused test. Explain why preserving source identity is necessary but insufficient for verifying the source's claims. Record your own reasoning; completion is not assumed.

## Explain a bounded triage repair and its remaining failures

Read the [callback-denial comparison](../evidence/CALLBACK_DENIAL.md). Predict the routes for a denied callback alone, a denied callback plus a blank Offerwall, and a denied iOS callback plus a positive Android callback. Trace the signal occurrences that the rule excludes and retains, then compare your predictions with the frozen and current outputs.

The [interactive triage explorer](https://yuchi-wang02.github.io/csm-copilot/#triage-review) shows the same preserved cases. Use a repair, a positive control and a known limitation to explain what changed and what the rule still cannot establish. Its status compares categories with the project's expectations, not with independent ground truth.

Choose one remaining failure and explain why it falls outside the implemented pattern. Describe what a CSM should clarify instead of claiming that the system understands the sentence. Run `python -m pytest tests/test_callback_denial.py -q` and distinguish a passing regression suite from a general accuracy estimate. This is an exercise for your own reasoning; no personal completion is recorded.
