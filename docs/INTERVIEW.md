# A three-minute walkthrough

This is a suggested presentation, not a claim that the exercises or interview have already happened.

Use the [two-page PDF brief](../demo/project-brief.pdf) as a leave-behind or offline introduction. It includes clickable links to the examples and identifies the evidence bundle behind its figures.

For a targeted demonstration, use [direct links to the Android evidence, Chinese iOS follow-up, and Harbor handoff](SHARING.md). The selected platform and review step are preserved, so the audience opens the example you intend.

## 0:00–0:30 — Explain the customer problem

“I wanted to explore how AI could support customer onboarding while keeping the CSM accountable for the next step. In this example, a publisher wants to launch on Friday. iOS looks ready, but Android shows a blank offerwall. The challenge is to turn incomplete information into a useful follow-up without overpromising.”

Open the [case explorer](https://yuchi-wang02.github.io/csm-copilot/). Point out the fixed snapshot and synthetic data label.

The download links above the queue provide a portable review brief with findings, drafts, next actions and evidence. Use it as a leave-behind or backup when you cannot run the live demo.

## 0:30–1:10 — Show the evidence boundary

Select Lantern Games. Show Android's unknown currency approval and failed device check. Switch to iOS and back.

“The checklist is scoped to the app and platform. Passing on iOS does not prove Android is ready. I also separate an unknown state from an observed failure, because they lead to different customer questions.”

Open a source link or evidence record. Explain the difference between a documented product condition and a project operating policy.

## 1:10–1:50 — Move the work forward

Open Follow-up, switch to Chinese, then open Handoff.

“The draft asks for the missing evidence. The handoff includes what we know and makes missing fields visible. Neither action sends a message or updates the last-contact timestamp. The next owner can see what still needs to be collected.”

Show the counterfactual update. Two settings change, but the failed device check remains unresolved.

## 1:50–2:30 — Explain the AI architecture and failure cases

“The server exposes MCP tools so a model-enabled host can orchestrate the workflow. Dates and checklist rules stay deterministic. This website replays engine outputs and separately recorded local model attempts. The initial batch attempt chose all four requested calls but overstated the evidence. The constrained attempt matched structured fields after two recorded corrections; its prose still needs review. I distinguish tool coverage from answer fidelity.”

Show the 14/18 lexical diagnostic result and two failure families. For the AI-specific extension, open [the recorded local model run](LOCAL_MODEL.md): it completed four tool calls but overstated the evidence in its final response. Explain why successful tool use and faithful summarization need separate checks.


## 2:30–3:00 — Explain the learning direction honestly

“The project connects my interest in business analytics, customer communication and process controls. I used substantial AI assistance for implementation. My next learning goal is to trace each tool, explain the tests, and implement a small improvement that I can defend myself.”

Replace the last sentence only after completing and documenting the relevant exercises. Do not claim personal implementation of a component you cannot explain.

## Questions to prepare for

| Interviewer question | A defensible answer |
|---|---|
| Why MCP? | It gives model-enabled clients a typed interface to a reusable workflow; it is not itself the language model. |
| Why not let the LLM decide readiness? | Evidence state and scope should remain inspectable; the model can explain them without silently changing the rule. |
| Is this production-ready? | No. It lacks real CRM integration, auth, conflict resolution, freshness policy and human outcome validation. |
| What did you measure? | Synthetic category-set retrieval and workflow behavior; not time savings or customer success outcomes. |
| How do you know a draft is factual? | Its template is tied to structured records, but regex lint is insufficient for arbitrary model rewrites. Human claim-to-evidence review remains necessary. |
| What would you improve first? | Independent cases and human review of model-written claims, then semantic retrieval compared fairly to the baseline. |

## Portfolio wording

For a Product-focused interview, add a one-minute extension: open [Product feedback](https://yuchi-wang02.github.io/csm-copilot/#feedback), compare the two device-verification accounts, and explain why a failed test and a missing record lead to a question rather than a defect claim. The [exercise](PRODUCT_FEEDBACK.md) covers account deduplication and applicable denominators.

Safe current description:

> Developed an AI-assisted portfolio prototype of an evidence-grounded CSM onboarding workflow, with an eight-tool MCP server, bilingual follow-up templates, an interactive case explorer, and reproducible synthetic diagnostics that expose failure modes.

Avoid adding production adoption, customer impact, measured efficiency gains or independent human evaluation without new evidence.

## v0.6 demonstration exercise

Open the "Qwen3-4B · constrained JSON + field review" attempt. Explain the initial source-role error and repeated platform entries, then show the two correction requests and final matching fields. Expand the system-rendered evidence summary. Identify why it is different from the model explanation, and find the missing inline citations and nothing-sent sentence in that explanation. [Response-review design](RESPONSE_REVIEW.md).

Describe the work as an AI-assisted development experiment with inspectable failures. Personal mastery is demonstrated when you can trace a rejection to its source, predict a new failure case, and explain or implement a small change yourself; it is not established by the number of tests or iterations in the repository.

## Optional audience interaction

For an AI-tool discussion, compare the two callback handoff recordings. The model supplies the same issue ID as triage prose in both. The earlier server accepts it; the newer server rejects it with a useful error while the recorded-issue handoff still succeeds. Explain the narrow exact-match rule and then identify what the newer answer still omits: evidence citations, the proposed owner and the specific hypothesis. This demonstrates a failure-to-control development sequence without claiming that the whole answer became reliable.

Open [Practice](https://yuchi-wang02.github.io/csm-copilot/#practice) and invite the interviewer to choose a next action for the Android update. Explain the distinction between a failed check and an unknown check before showing the guidance. For an AI-focused discussion, use the third decision and identify the remaining omissions in the model explanation. This is a short conversation aid with published answers, not a quiz score to present as professional qualification.
