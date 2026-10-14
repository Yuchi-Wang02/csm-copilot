# Architecture and decisions

## A small system with a visible evidence boundary

`Account → Integration (app + platform + currency mode) → Fact → Evidence`

Issues refer to an integration and a customer evidence record. Contact timestamps refer only to actual contact records. The JSON fixture is validated with Pydantic before any tool reads it. Broken identifiers, duplicate IDs, timezone-free timestamps, future evidence and unsupported known facts fail validation.

The engine uses an immutable-by-convention in-memory snapshot loaded from packaged JSON. Its public tools do not mutate it. A database would add migrations and state management without improving this five-account demonstration. Persistent CRM storage belongs in a later integration.

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
| No friction counters in v0.1 | Repeated tool calls must not manufacture customer incidents | Product-feedback aggregation is deferred |

## Readiness aggregation

1. A required check with `not_met` makes the integration `blocked`.
2. Otherwise an `unknown` check makes it `needs_evidence`.
3. Otherwise the scoped checklist is `checklist_complete`.
4. Self-managed callback verification is `not_applicable` for Tapjoy-managed currency. No other required check can be waived with an input `not_applicable` status; it becomes `unknown`.

Each result includes rule version, source URL, authority type and evidence IDs. The current fixture explicitly records facts. It does **not** use a model to extract facts from arbitrary customer prose, resolve conflicting records or verify dashboard screenshots. A known fact means “supported by the recorded synthetic source,” not externally confirmed truth.

## Priority and time

`contact_age_days = (as_of - latest_actual_contact) / 86,400 seconds`

Selection uses a strict `>` threshold. Missing contact history is included with `contact_state: unknown`. Live accounts are excluded by default and never shown as pending-launch overdue. Selected accounts are ordered by target launch date; this is a simple project policy, not a predictive risk score or revenue-weighted business prioritizer.

## What each layer owns

- **Schema:** referential integrity, known fact evidence and timestamp constraints.
- **Engine:** retrieval, deterministic rules, structured draft assembly.
- **MCP adapter:** typed tool schemas, read-only annotations and workflow prompt.
- **MCP host:** natural-language interpretation, tool choice, optional draft rewriting.
- **Human:** evidence adequacy, nuanced customer judgment and final communication.
- **Static explorer:** exact generated outputs; no fabricated model activity.

## Counterfactual updates

The demo makes a separate copy of the original dataset, appends a customer report and updates two Android facts in that copy. Historical evidence remains available. The last recorded device failure is not silently replaced by a pass. The example illustrates partial information updates, not a general event-sourced CRM or production conflict-resolution engine.

## Extending responsibly

A next iteration should add separately authored cases and a model-enabled host trace before expanding product coverage. For real CRM integration, add authorization, evidence freshness, conflict review, idempotency keys, a separate draft/sent state machine and a reviewable send action. The current code intentionally has no external send capability.
