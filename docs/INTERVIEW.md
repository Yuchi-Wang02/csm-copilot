# A three-minute walkthrough

This is a suggested presentation, not a claim that the exercises or interview have already happened.

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

“The server exposes MCP tools so a model-enabled host can orchestrate the workflow. Dates and checklist rules stay deterministic. This website is a replay of the same engine outputs. I verified the real MCP transport with a scripted client; I have not measured live model orchestration quality.”

Show the 14/18 diagnostic result and two failure families.

“The lexical baseline misses indirect wording and misreads negation. That is useful evidence for the next iteration. I would compare a semantic approach on separately written cases, with the same information available to each baseline.”

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
| What would you improve first? | Independent cases and a recorded model-enabled workflow run, then semantic retrieval compared fairly to the baseline. |

## Portfolio wording

Safe current description:

> Developed an AI-assisted portfolio prototype of an evidence-grounded CSM onboarding workflow, with a seven-tool MCP server, bilingual follow-up templates, an interactive case explorer, and reproducible synthetic diagnostics that expose failure modes.

Avoid adding production adoption, customer impact, measured efficiency gains or independent human evaluation without new evidence.
