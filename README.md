> Independent portfolio project. Not affiliated with, endorsed by, or connected to Unity. All customer records are synthetic.

# CSM Copilot

**Move customer onboarding forward without turning uncertainty into a promise.**

A customer-success portfolio by **Yuchi Wang**: a working Model Context Protocol (MCP) server and interactive case explorer that turn account evidence into bilingual follow-ups and technical handoffs.

**[Start the three-minute review](https://yuchi-wang02.github.io/csm-copilot/#start)** · **[Project brief (PDF)](demo/project-brief.pdf)** · **[Interview walkthrough](docs/INTERVIEW.md)** · **[Run locally](docs/LOCAL_SETUP.md)**

[![Morning review with three queued accounts and an Android follow-up requesting missing confirmations, a fresh device check, and callback evidence. The draft is explicitly unsent.](docs/assets/workflow-0ea4b88.jpg)](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=followup&lang=en#workspace)

Workflow screenshot from [source revision 0ea4b88](https://github.com/Yuchi-Wang02/csm-copilot/commit/0ea4b88a0d4a1a4c1a4ea364440960563ddf39b6). The website replays Python workflow outputs and saved model attempts; it does not run a live AI chat or send messages.

[![Verify workflow](https://github.com/Yuchi-Wang02/csm-copilot/actions/workflows/ci.yml/badge.svg)](https://github.com/Yuchi-Wang02/csm-copilot/actions/workflows/ci.yml)
[![Publish case explorer](https://github.com/Yuchi-Wang02/csm-copilot/actions/workflows/pages.yml/badge.svg)](https://github.com/Yuchi-Wang02/csm-copilot/actions/workflows/pages.yml)

## The business problem

A publisher wants to launch on Friday. An iOS test passed, but a non-test Android device shows a blank Offerwall. The CSM needs to decide what to ask the customer, what to document, and when to involve technical support.

The prototype follows that work across **five fictional accounts and six app/platform integrations**, covering Offerwall onboarding, blank-offerwall reports and reward callbacks. It preserves the difference between a recorded failure, missing evidence and a possible explanation.

## Start with one case

1. **[Inspect Android](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en#workspace).** Currency approval and Test Only are unknown; the device check is recorded as not met. Expand the source view to read the dated evidence.
2. **[Read the next customer question](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=followup&lang=en#workspace).** The draft asks for missing confirmations and a fresh device result. Switch to Chinese, then inspect the handoff's missing fields.
3. **[Compare iOS](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_ios&view=followup&lang=en#workspace).** Its separate checklist is complete, so the next action is a launch-plan review. Completion is not launch approval.
4. **[Add fresh evidence](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en&update=2#customer-update).** Passing new checks changes the Android follow-up to an issue-status question; it does not automatically close the earlier complaint.

Every draft remains unsent. Drafting does not update contact history. Review dates and source dates stay distinct: moving the review clock forward does not refresh customer records.

## Where AI fits

**CSM request → AI host → scoped tools → results returned to the AI host → human review**

An AI host can choose tools and rewrite drafts. The Python server handles dates, platform scope, checklist states and source references deterministically. Its default drafts are templates, so the workflow can run without a model or API key.

The repository preserves **seventeen local Qwen attempts across four prescribed tasks**. In one, four tool calls succeeded but the explanation described iOS as having “full compliance.” Later host-assisted corrections brought structured fields into agreement with tool results; free prose still required review. The [first queue-first attempt](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-review#model-runs), [dependency-instruction attempt](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-sequenced#model-runs) and [policy-enabled attempt](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-enforced#model-runs) all stopped at batch parsing before any tool executed. These are exploratory attempts with changing prompts and settings, not an independent benchmark.

The deterministic workflow is the working baseline: it already selects accounts, checks readiness and assembles drafts. The model experiments explore tool orchestration and explanation. The platform task supplies both integration IDs, so its successful calls do not demonstrate autonomous account discovery. No comparison has established that adding the model saves time or improves customer outcomes. [Inspect the division of work and the evidence for it](docs/ARCHITECTURE.md#what-the-model-layer-contributes).

The [host policy and constrained generation](docs/DEPENDENCY_POLICY.md) now restrict each turn to pending work and IDs returned by earlier tools. A [new assisted morning run](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-constrained#model-runs) completed all seven requested calls: queue, context, two readiness checks, two English drafts and one handoff. The host then timed out waiting for the final explanation, so no model-written answer is claimed. The replay exposes the supplied state, decoding schemas, actual tool returns and terminal error. This provides an inspectable failure-to-test-to-fix-and-retest example while keeping tool completion separate from answer quality.

The host now [saves requests before dispatch and records specific timeout causes](docs/LOCAL_MODEL.md#preserve-a-request-before-waiting-for-its-response). A [subsequent run with a 600-second response budget](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-long-budget#model-runs) completed the seven calls and returned an 80-word explanation after 272.986 seconds of final generation. It correctly names the missing handoff fields but describes unknown currency approval and a recorded failed device check together as missing verification. Two excerpt-to-field comparisons make the supported and problematic wording inspectable. This is a completed assisted execution, with reasoning and citation gaps still visible.

[Inspect the original AI mistake](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-batch#model-runs) · [Follow the recorded corrections](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-constrained#model-runs) · [Read the raw-run review](evidence/MODEL_RUNS.md)

An [optional morning final-answer checker](docs/MORNING_FINAL.md) now requests separate unknown/failed checks, follow-up purposes, selected-account facts and handoff gaps. It compares those fields with observed calls and renders a separate summary on agreement. The [first actual run with this mode](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-field-review#model-runs) separates the evidence states but is rejected for including an issue report among readiness citations. The ID is real and correctly scoped; its evidentiary purpose is wrong for that field. No correction is attempted, and free prose still requires review.

An [optional final-context reduction](docs/MORNING_FINAL.md#optional-final-context-reduction) removes superseded host planning messages while preserving every tool result and an exact omission audit. A [new recorded attempt](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-compact-context#model-runs) reduces the final input from 9,386 to 7,728 tokens and records 94.323 seconds of final generation versus 405.461 previously. Its structured fields retain the same rejected citation. This is a runtime observation from one development pair, not a general speedup or an answer-quality improvement.

[![Two saved model claims compared with recorded tool results: iOS full compliance overstates a scoped checklist, and Android missing evidence omits a recorded unmet device check.](docs/assets/ai-claim-review-0ea4b88.jpg)](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-batch#model-runs)

Comparison screenshot from the same source revision. The assessment is an AI-assisted review of a saved attempt; open the replay to locate each field in its raw trace.

## Choose what to inspect

| Reviewer question | Evidence to open |
|---|---|
| Why was this account selected for review? | [Lantern's queue evidence](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en#workspace): expand **Why this account is in the queue** to inspect its contact record, threshold and fixed review time |
| Can the workflow prepare a useful technical handoff? | [Harbor callback case](https://yuchi-wang02.github.io/csm-copilot/?case=harbor_android&view=handoff&lang=en#workspace): request missing reproduction steps and redacted logs while retaining the supplied details |
| Can a CSM explain the next step to a publisher? | [Customer-education example](docs/CLIENT_EDUCATION.md) and [one-page teaching handout](demo/publisher-teaching-example.pdf) |
| Can recurring gaps become useful Product questions? | [Feedback review](https://yuchi-wang02.github.io/csm-copilot/#feedback): distinct account counts, source records and a proposed validation step |
| Can the system keep evidence in the right scope? | [Evidence probes](https://yuchi-wang02.github.io/csm-copilot/#integrity) and [the failure and fix](docs/EVIDENCE.md) |
| Can customer text authorize an action? | [Text/action probes](https://yuchi-wang02.github.io/csm-copilot/#trust-boundary), including remaining gaps |
| Can I explain the reasoning myself? | [Six practice decisions](https://yuchi-wang02.github.io/csm-copilot/#practice) and [learning exercises](docs/LEARNING.md) |

For presentation details, use the [interview walkthrough](docs/INTERVIEW.md). For a portable replay, download the fixed [v0.30.0 interview package](https://github.com/Yuchi-Wang02/csm-copilot/releases/tag/v0.30.0); the [package guide](docs/INTERVIEW_BUNDLE.md) distinguishes that release from newer source changes. [Sharing instructions](docs/SHARING.md) cover direct links, platform briefs and practice exports.

## Tools

All eight MCP tools are read-only. The two prompts compose a morning review and a Product-feedback discussion.

| Tool | Role in the workflow |
|---|---|
| `list_accounts` | Queue stale contacts and unknown-contact entries; prioritize planned launches |
| `get_account_context` | Read an account's integrations, issues and attributed evidence |
| `check_readiness` | Evaluate each app/platform separately; preserve unknown and unmet checks |
| `triage_issue` | Retrieve possible checks and questions using a lexical baseline |
| `draft_ticket` | Prepare a technical handoff with explicit missing fields |
| `draft_followup` | Produce an English or Chinese template for the current next action |
| `validate_draft` | Flag narrow promise patterns; this does not verify factual support |
| `friction_digest` | Turn snapshot gaps into proposed Product questions, without diagnosing defects |

[MCP setup and prompts](docs/MCP.md) · [Actual protocol transcript](evidence/mcp-transcript.json) · [Architecture and decisions](docs/ARCHITECTURE.md)

## What the evaluation actually shows

| Evidence | Observed result | Interpretation |
|---|---|---|
| Synthetic triage messages | 12/12 development; 16/18 reused cases, previously 14/18 | Rules were adapted after inspecting failures; the latter result is not a fresh holdout |
| Eight promise-lint probes | 4 true positives, 2 false negatives, 1 false positive, 1 true negative | Fluent unsupported claims can pass; one negated promise is flagged |
| Scripted MCP client | Eight tools and both prompts retrieved over real stdio | Protocol integration, separate from model tool choice |
| Windows and Linux CI | Workflow, browser-logic, export and installed-package checks | Reproducible authored cases; see the badges for current run status |

Known failures remain visible, including indirect wording, qualified negation and quoted topics. There is no independent human validation, measured customer impact or general model-reliability estimate.

[Methodology and results](evidence/EVALUATION.md) · [Verification scope](docs/VERIFICATION.md) · [Before/after triage explorer](https://yuchi-wang02.github.io/csm-copilot/#triage-review) · [Detailed development history](docs/DEVELOPMENT.md)

## Portfolio rationale

This project connects customer communication, business analytics and process controls. It makes a chain of decisions inspectable: identify the account, separate evidence from assumptions, ask a focused question, prepare a handoff, and review what an AI explanation adds.

**Contribution transparency:** Yuchi selected the direction, intended audience and CSM workflow, and commissioned the build. Implementation, tests, documentation and synthetic cases used substantial AI assistance. Unaided coding, completed personal mastery exercises and independent customer validation are not claimed.

The [learning path](docs/LEARNING.md) asks you to predict a result, change a copied input, inspect the output and explain the difference. [Practice](https://yuchi-wang02.github.io/csm-copilot/#practice) keeps initial reasoning separate from later reflection, with local save/resume and export. Those responses can provide a concrete basis for discussing your own learning.

## Run locally

To present the committed browser replay, follow the [local preview commands](docs/LOCAL_SETUP.md#view-the-browser-replay); no package installation or model is needed. To execute the workflow, use Python **3.11–3.13** and [install the Python package](docs/LOCAL_SETUP.md#install-the-python-workflow), then print a morning summary or export English/Chinese briefs. The [full verification sequence](docs/VERIFICATION.md#reproduction) includes JavaScript checks, package checks and PDF builders.

## Repository map

```text
src/csm_copilot/   Evidence schema, workflow engine, MCP server and fixtures
demo/             Interactive replay, downloadable briefs and PDFs
tests/, tests-js/  Authored behavior and boundary checks
evaluation/       Synthetic diagnostic cases and evaluators
evidence/         Workflow outputs, protocol transcript and model recordings
docs/             Sources, methods, setup, interview and learning guides
scripts/          Builders and protocol/package verification
```

Public sources are paraphrased and linked in the [source register](docs/SOURCES.md), reviewed **2026-10-14**. Project policies are labeled separately from official product guidance. See [limitations and data handling](docs/LIMITATIONS.md) before extending the prototype. Code is MIT licensed; referenced vendor documentation retains its own terms.
