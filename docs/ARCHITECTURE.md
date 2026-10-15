# Architecture and decisions

## A small system with a visible evidence boundary

`Account → Integration (app + platform + currency mode) → Fact → Evidence`

Issues refer to an integration and a customer evidence record. Contact timestamps refer only to actual contact records. The JSON fixture is validated with Pydantic before any tool reads it. Broken identifiers, duplicate IDs, timezone-free timestamps, future evidence and unsupported known facts fail validation.

The engine uses an immutable-by-convention in-memory snapshot loaded from packaged JSON. Its public tools do not mutate it. A database would add migrations and state management without improving this five-account demonstration. Persistent CRM storage belongs in a later integration.

Since v0.8.1, constructing an engine from a caller-owned `Dataset` revalidates its current contents and creates a separate snapshot. Readiness results copy evidence-ID lists, including those consumed by the Product digest. Editing these returned lists or the original constructor input cannot change later engine results. This protects ordinary in-process use; it does not prevent deliberate mutation of the engine's own public attributes. MCP clients already receive separately serialized JSON objects.

Since v0.2, evidence declares account/integration ownership and structured check claims. Validation rejects cross-account contacts, cross-platform or wrong-check citations, and known facts that contradict their referenced claims. Ticket detail fields cannot overwrite integration identity; each output field carries a source pointer. These constraints validate declared provenance, not the truth of the underlying text. See [evidence boundaries](EVIDENCE.md).

## Decisions that matter

| Decision | Reason | Tradeoff |
|---|---|---|
| App/platform readiness, not account readiness | iOS evidence must not certify Android | More records to maintain |
| Four check states | Missing information differs from observed failure | Overall status must preserve uncertainty |
| `checklist_complete`, not `approved` | A scoped project checklist cannot authorize launch | User must understand scope |
| Project-policy checks labeled separately | Device/reward verification is our operating choice | More metadata in each result |
| Fixed timezone-aware snapshot | Same queue and demo on every machine | Live usage needs an explicit current timestamp and refreshed evidence |
| Read-only tools and draft-only outputs | Drafting cannot fabricate contact history | Sending and CRM writes are outside v0.1 |
| Deterministic dates and checklist logic | Arithmetic and state rules are auditable | Rules do not understand nuanced prose |
| Lexical triage baseline | Cheap, inspectable starting point for semantic retrieval comparison | Known negation/paraphrase failures |
| Host-owned model | Standard MCP interface without a second model bill | Actual host behavior must be evaluated separately |
| Snapshot feedback aggregation | Repeated tool calls must not manufacture customer incidents | v0.4 aggregates existing checklist states, not new customer events |

## What the model layer contributes

The optional local host has a [morning-review dependency policy and constrained-generation mode](DEPENDENCY_POLICY.md). It derives pending work from successful queue/context results, validates proposals before execution and requires that work before accepting a final response. The host supplies pending-action state and can restrict decoding to one permitted action. Scripted-worker tests exercise the real MCP transport. The thirteenth model recording enables the policy but stops at parsing; the fourteenth adds decoding constraints and completes seven tool calls, then times out before a final answer. A fifteenth recording uses a 600-second response budget and saves each full request before dispatch. It completes seven calls and returns a final answer, but the explanation conflates unknown and failed checks; its [claim-to-field comparison](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-long-budget#model-runs) shows the gap. This scope applies to the custom host, not arbitrary MCP clients, and does not validate final prose.

The deterministic workflow is a usable baseline for this fixed task. [build_demo](../src/csm_copilot/demo.py) selects the queue, obtains account context, checks each integration and assembles bilingual follow-ups and handoffs without a model. The CLI and static explorer make those outputs reviewable. A model is not required to perform the arithmetic, apply the checklist or fill the existing templates.

The model layer explores whether a natural-language request can lead to appropriate tool calls and a useful explanation. The recordings support narrower observations:

| Work being examined | What the tools already supply | What the recorded model did | What remains unproven |
|---|---|---|---|
| Two-platform follow-up | Scoped readiness, source references and a template for each platform | The [batch attempt](../evidence/model-runs/qwen4-batch.json) executed the four requested calls, then added an explanation that overstated iOS compliance and misrepresented Android evidence | Better communication, time savings or autonomous account discovery; the task explicitly supplied both integration IDs |
| Two unrelated inbound messages | Lexical candidates, routes and clarification questions | The [neutral-question attempt](../evidence/model-runs/qwen4-triage-neutral-questions.json) called triage for each supplied message and incorporated the returned questions into its explanation | General intent understanding or a verified billing workflow; the exact messages were prescribed and the tool's invoice questions remained broad |
| Recovery after an output error | Host checks against observed structured tool results and correction feedback | The [constrained attempt](../evidence/model-runs/qwen4-constrained.json) matched structured fields after two host correction requests | Independent self-correction or faithful free prose; the feedback supplied expected values and the explanation still required review |
| Queue-first morning review | A snapshot queue ordered by planned launch, account context, scoped drafts and host-derived action schemas | Earlier attempts failed before execution or timed out. The [explanation-checklist attempt](../evidence/model-runs/qwen4-morning-explanation-checklist.json) completes seven calls and matches final fields after supplied citation feedback; its prose still omits next actions and citations | Unaided planning and useful customer communication; the host restricts allowed tool/ID combinations and supplies writing/correction assistance |

These are role attributions within saved runs, not a controlled comparison between a human, a deterministic script and an AI assistant. Tool coverage measures the requested actions observed in that recording. It does not measure customer usefulness or the truth of the source records. Later queue-first recordings complete the seven calls using IDs returned by tools, with host-supplied dependency state and constrained actions. The nineteenth recording also returns matching structured fields after supplied correction feedback, while its explanation remains incomplete. This demonstrates assisted execution, not unaided planning or a verified customer-ready answer.

In an interview, explain the intended benefit as a hypothesis: a conversational layer might make an established workflow easier to access or summarize. Then show the observed cost of that layer—an unsupported claim—and how a reviewer can trace it back to the tool result. A future usefulness comparison would need separately defined tasks, a baseline, independent review and an explicit measure of useful output or effort. None has been completed here. [Learning Session 3](LEARNING.md#session-3--understand-the-mcp-boundary-45-minutes) provides a no-model protocol exercise before comparing an actual model recording.

The optional [morning final-answer contract](MORNING_FINAL.md) composes the dependency-policy replay with the existing readiness-field reviewer. It derives scope from observed queue/context results, adds selection, follow-up-purpose and handoff checks, and renders a separate summary on agreement. The host supplies the new contract after tool completion; scripted integration tests preserve the preceding seven requests. The [sixteenth recording](../evidence/model-runs/qwen4-morning-field-review.json) exercises this path: its answer separates unknown and failed checks, but field review rejects an issue-only readiness citation and withholds the checked summary. This is field checking, not a semantic validator of model prose.

## Readiness aggregation

1. A required check with `not_met` makes the integration `blocked`.
2. Otherwise an `unknown` check makes it `needs_evidence`.
3. Otherwise the scoped checklist is `checklist_complete`.
4. Self-managed callback verification is `not_applicable` for Tapjoy-managed currency. No other required check can be waived with an input `not_applicable` status; it becomes `unknown`.

Each result includes rule version, source URL, authority type and evidence IDs. The current fixture explicitly records facts. It does **not** use a model to extract facts from arbitrary customer prose, resolve conflicting records or verify dashboard screenshots. A known fact means “supported by the recorded synthetic source,” not externally confirmed truth.

Triage accepts customer prose, whereas ticket drafting accepts a recorded issue ID. Since v0.9.1, a bare known issue ID supplied as triage text is rejected with guidance to retrieve its message or use `draft_ticket`. This exact-match check does not classify arbitrary strings as identifiers or provide general semantic input validation.

Since v0.10.1, English no-offers phrases use Latin-letter boundaries to avoid substrings such as `blank` in `blanket` and `no offers` in `casino offers`. Common blank forms and plural offerwalls are retained. ASCII letter boundaries allow Chinese text directly beside English signals; they are not a general multilingual tokenizer. Chinese signals and reward/callback retrieval are unchanged. Negation, quoted symptoms and indirect wording still need human review. See the [paired development probes](../evidence/TRIAGE_BOUNDARIES.md).

## Priority and time

`contact_age_days = (as_of - latest_actual_contact) / 86,400 seconds`

Selection uses a strict `>` threshold. Missing contact history is included with `contact_state: unknown`. Live accounts are excluded by default and never shown as pending-launch overdue. Selected non-live accounts are ordered by the exact timezone-aware target launch timestamp, with account ID breaking actual timestamp ties. Optional live accounts follow the non-live queue. Rounded `days_to_launch` values are for display only: rounding can collapse launches minutes apart into an artificial tie. This is a simple project policy, not a predictive risk score or revenue-weighted business prioritizer.

The queue returns `dataset_as_of` separately from its calculation `as_of`. A later date is labeled `recalculated_from_snapshot` with `records_refreshed: false`; it does not update contacts, stages, launch plans or checklist evidence. Different timezone offsets representing the same instant remain `dataset_snapshot`. Empty date strings are rejected rather than silently selecting the snapshot.

## What each layer owns

- **Schema:** referential integrity, known fact evidence and timestamp constraints.
- **Engine:** retrieval, deterministic rules, structured draft assembly.
- **MCP adapter:** typed tool schemas, read-only annotations and workflow prompt.
- **MCP host:** natural-language interpretation, tool choice, optional draft rewriting.
- **Human:** evidence adequacy, nuanced customer judgment and final communication.
- **Static explorer:** exact generated outputs; no fabricated model activity.
- **Issue display:** all recorded issues for the selected integration, each paired with its own source and handoff; missing associated records are explicit.
- **Readable export:** the same workflow packet rendered into a portable Markdown brief, with draft purpose, next actions and source records.

Follow-up intent is chosen from checklist state, recorded issues and the supplied account stage. A complete checklist with a recorded issue prompts a status question; it does not close the issue automatically. Complete handoffs move to review rather than requesting information already supplied. See [the communication and export policy](REVIEW_BRIEF.md).

Handoff scope and field completeness are separate decisions. Since v0.8.2, a triage result of `clarify_scope` produces `needs_scope`, with the CSM as the proposed owner, even when every generic field is present. Recognized candidates with missing fields produce `needs_information`; recognized candidates with complete fields produce `ready_for_human_review`. Missing generic fields remain visible in the structured result, but the browser asks for scope clarification before requesting technical details. A lexical match only suggests a candidate: neither recognition nor complete fields confirms a cause or authorizes submission.

## Counterfactual updates

The [Android comparison](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en&update=2#customer-update) has three views built from separate snapshots. The original morning-review packet stays unchanged. Each added record belongs to the same account and Android integration, and constructing the copied engine revalidates the evidence references.

| View | Evidence change | Scoped checklist result | CSM implication |
|---|---|---|---|
| Original snapshot | No new record | `blocked`: two met, three unknown, one not met | Ask for missing confirmations and a fresh device check |
| Settings confirmed | `reply_android_settings` supports currency approval and Test Only being off | Still `blocked`: four met, one unknown, one not met | Those two confirmations do not establish a new device result or callback check |
| Fresh checks pass | `fresh_android_checks` supports both device and callback checks in a copy of the settings-confirmed snapshot | `checklist_complete`: six met | The generated follow-up changes to `issue_status_review`, asking whether the earlier issue still occurs |

The passing branch retains `issue_blank` and its original source record. It does not mark the issue open or resolved: this prototype has no issue-resolution lifecycle. It also preserves the account record and prior evidence, sends nothing and leaves contact history unchanged. The new test record supports the changed facts; it does not erase the earlier failed observation or establish launch approval.

These are authored synthetic branches at the fixed snapshot, not an automatic reconciliation process. The code explicitly selects which facts the new record supports. Read the [branch construction](../src/csm_copilot/demo.py), [generated packet](../evidence/workflow.json) and [behavior checks](../tests/test_update_story.py) together. The [follow-up policy](REVIEW_BRIEF.md#four-distinct-follow-up-purposes) explains why complete checks can still lead to a customer question. The original case panel and downloaded briefs continue to use the original snapshot; the toggle changes only the separate comparison.

## Extending responsibly

Version 0.5 adds local model traces with visible answer failures. A next iteration should add separately authored cases and independent claim review before expanding product coverage. For real CRM integration, add authorization, evidence freshness, conflict review, idempotency keys, a separate draft/sent state machine and a reviewable send action. The current code intentionally has no external send capability.

## Portfolio feedback aggregation

`friction.py` consumes `check_readiness` results across the selected account cohort. Applicability therefore comes from the same rules as customer review. It aggregates once per integration/check, deduplicates accounts within each theme, and retains source records. `friction_digest` exposes the result through MCP; `product_feedback_review` provides the host prompt. The browser and Markdown export share the generated `evidence/friction.json` payload. Product questions are explicit project proposals, not inferred root causes.
