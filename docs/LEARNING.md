# Learning path: make the project yours

The project is a starting point for demonstrated understanding. These exercises are **not marked complete**. Keep personal notes and small commits as you work through them; that is stronger evidence of learning than an oversized feature list.

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

Open the latest recorded attempt. Explain the initial source-role error and repeated platform entries, then show the two correction requests and final matching fields. Expand the system-rendered evidence summary. Identify why it is different from the model explanation, and find the missing inline citations and nothing-sent sentence in that explanation. [Response-review design](RESPONSE_REVIEW.md).

Describe the work as an AI-assisted development experiment with inspectable failures. Personal mastery is demonstrated when you can trace a rejection to its source, predict a new failure case, and explain or implement a small change yourself; it is not established by the number of tests or iterations in the repository.

## v0.7: keep a before-and-after reflection

Use [the interactive practice](PRACTICE.md) to choose an action and explain your reasoning before revealing guidance. The download keeps that original response separate from your later reflection. These are your notes, not an automated evaluation. Complete the exercise yourself before describing it as personal learning evidence. The public site and repository contain no claimed completion by Yuchi.
