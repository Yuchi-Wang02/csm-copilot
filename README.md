> Independent portfolio project. Not affiliated with, endorsed by, or connected to Unity. All customer records are synthetic.

# CSM Copilot

**Move customer onboarding forward without turning uncertainty into a promise.**

A customer-success portfolio by **Yuchi Wang**. A Python workflow and Model Context Protocol (MCP) server turn incomplete account evidence into bilingual follow-ups and technical handoffs.

**[Explore the three-minute demo →](https://yuchi-wang02.github.io/csm-copilot/#start)** · **[Project brief (PDF)](demo/project-brief.pdf)** · **[Interview walkthrough](docs/INTERVIEW.md)**

[![Verify workflow](https://github.com/Yuchi-Wang02/csm-copilot/actions/workflows/ci.yml/badge.svg)](https://github.com/Yuchi-Wang02/csm-copilot/actions/workflows/ci.yml)
[![Publish case explorer](https://github.com/Yuchi-Wang02/csm-copilot/actions/workflows/pages.yml/badge.svg)](https://github.com/Yuchi-Wang02/csm-copilot/actions/workflows/pages.yml)

[![Review queue and an Android follow-up requesting missing confirmations, a fresh device check and callback evidence. The draft is unsent.](docs/assets/workflow-0ea4b88.jpg)](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=followup&lang=en#workspace)

Workflow preview from [revision 0ea4b88](https://github.com/Yuchi-Wang02/csm-copilot/commit/0ea4b88a0d4a1a4c1a4ea364440960563ddf39b6). **The website replays saved outputs; it does not run a live AI chat or send messages.**

## The business problem

A publisher wants to launch on Friday. iOS checks are complete, but a non-test Android device shows a blank Offerwall. The CSM needs a focused customer question, a clear technical handoff and a record of what remains uncertain.

The prototype covers **five fictional accounts and six app/platform integrations**. It separates missing evidence from a recorded failure and keeps each platform's conclusions tied to its own sources.

## Start with one case

| Step | Open the evidence | What to look for |
|---|---|---|
| 1. Decide what to ask | [Android follow-up](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=followup&lang=en#workspace) | Unknown settings require confirmation; a failed device check requires a fresh test. Switch between English and Chinese. |
| 2. Prepare the handoff | [Android issue](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=handoff&lang=en#workspace) | Retain supplied details; request the SDK version, time window and redacted logs. Keep the root cause unconfirmed. |
| 3. Compare the next action | [iOS follow-up](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_ios&view=followup&lang=en#workspace) | Its complete checklist leads to launch-plan review, not launch approval. |

Then [add fresh Android evidence](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en&update=2#customer-update): passing checks changes the next question without automatically resolving the earlier complaint. Drafts remain unsent and contact history stays unchanged.

## Where AI fits

| Layer | Responsibility |
|---|---|
| Python tools | Select accounts, calculate dates, apply scoped checklist rules and assemble draft templates. Works without a model or API key. |
| Optional AI host | Propose tool calls and write explanations. Later recorded workflows use explicit host constraints and correction feedback. |
| Human reviewer | Judge evidence adequacy, tailor communication and decide what to do next. |

**One finding worth inspecting:** a model completed four requested tool calls, then described a scoped iOS checklist as “full compliance.” [Compare its words with the recorded result →](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-batch#model-runs)

The repository preserves **19 local Qwen attempts across four prescribed tasks**, including failures and assisted corrections. Later morning runs complete seven calls, but matching structured fields still leaves gaps in the explanation. These are exploratory development records, not a controlled benchmark. [Browse the experiments](evidence/MODEL_RUNS.md) · [Inspect the division of work](docs/ARCHITECTURE.md#what-the-model-layer-contributes)

## What the evaluation actually shows

- **Triage:** 12/12 development cases and 16/18 reused cases match the authored categories. Inspected failures informed rule changes; this is not independent accuracy.
- **Promise checks:** eight diagnostic probes include false positives and false negatives. Zero flags does not establish factuality.
- **Engineering:** Windows and Ubuntu CI check workflow behavior, browser logic, real MCP transport, generated artifacts and installed packages. Use the badges above for current status.

No independent human validation, measured customer benefit or production readiness is claimed. [Evaluation](evidence/EVALUATION.md) · [Verification scope](docs/VERIFICATION.md) · [Limitations](docs/LIMITATIONS.md)

## Portfolio rationale

This project connects customer communication, business analytics and process controls. **Yuchi selected the direction, audience and CSM workflow.** Implementation, tests, documentation and synthetic cases used substantial AI assistance; unaided implementation and completed personal mastery are not claimed.

The [learning path](docs/LEARNING.md) turns the project into three concrete exercises: explain one customer decision, trace one AI mistake and run one experiment on a copied dataset. [Six interactive practice decisions](https://yuchi-wang02.github.io/csm-copilot/#practice) keep initial reasoning separate from reflection.

## Explore or reproduce

| Your goal | Start here |
|---|---|
| Present the project | [Three-minute walkthrough](docs/INTERVIEW.md) and [project PDF](demo/project-brief.pdf) |
| Explain a product question | [Customer-education example](docs/CLIENT_EDUCATION.md) and [one-page handout](demo/publisher-teaching-example.pdf) |
| Connect cases to Product | [Feedback review](https://yuchi-wang02.github.io/csm-copilot/#feedback): attributed gaps and questions to validate |
| Keep a fixed demo | [v0.30.2 interview package](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.30.2); [contents and checksum](docs/INTERVIEW_BUNDLE.md). The hosted site can be newer. |
| Run locally | [Setup guide](docs/LOCAL_SETUP.md): browser replay or Python 3.11–3.13 workflow; model optional |

<details>
<summary><strong>Technical map: tools, source and reproduction</strong></summary>

## Tools

Eight read-only MCP tools and two workflow prompts:

| Tool | Purpose |
|---|---|
| `list_accounts` | Select the follow-up queue |
| `get_account_context` | Retrieve integrations, issues and evidence |
| `check_readiness` | Evaluate each app/platform |
| `triage_issue` | Suggest checks and questions using a lexical baseline |
| `draft_ticket` | Prepare a handoff with explicit missing fields |
| `draft_followup` | Produce an English or Chinese template |
| `validate_draft` | Flag narrow promise patterns |
| `friction_digest` | Aggregate snapshot gaps into Product questions |

[MCP setup](docs/MCP.md) · [Protocol transcript](evidence/mcp-transcript.json) · [Architecture](docs/ARCHITECTURE.md) · [Full verification commands](docs/VERIFICATION.md#reproduction)

## Repository map

```text
src/csm_copilot/   Workflow engine, MCP server and synthetic fixtures
demo/             Interactive replay, briefs and PDFs
tests/, tests-js/  Authored behavior and boundary checks
evaluation/       Diagnostic cases and evaluators
evidence/         Outputs, protocol transcript and model recordings
docs/, scripts/   Methods, learning guides, builders and verification
```

[Evidence boundaries](docs/EVIDENCE.md) · [Development history](docs/DEVELOPMENT.md) · [Sharing guide](docs/SHARING.md)

</details>

Public guidance is paraphrased and cited in the [source register](docs/SOURCES.md), reviewed **2026-10-14**. Project policies are labeled separately. Code is MIT licensed; referenced documentation retains its own terms.
