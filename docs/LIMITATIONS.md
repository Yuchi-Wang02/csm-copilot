# Limits and data handling

This is an educational portfolio prototype with synthetic records, not a deployable customer-support product.

- **No real account integration.** JSON fixtures represent a fixed snapshot. No CRM, Unity dashboard, ticketing or messaging connection exists.
- **No live model evaluation.** A model-enabled MCP host can use the tools. The published demo and evaluations do not run a language model.
- **Triage is a baseline.** Lexical matches can miss paraphrases and misread negation; multiple symptoms are returned as candidates.
- **Evidence is attributed, not independently verified.** Known facts refer to fixture evidence. There is no screenshot verification, contradictory-evidence resolution or stale-evidence expiration policy.
- **Checklist scope is partial.** `checklist_complete` covers six project checks and never certifies production launch, compliance or revenue.
- **Promise lint is narrow.** Regex patterns have both false positives and false negatives. Absence of flags never establishes factuality.
- **Evaluation is synthetic and same-session authored.** Family separation helps prevent bilingual duplicate leakage but does not create independent human validation.
- **Drafting is read-only.** No records are sent or contact timestamps updated. A future write integration needs explicit authorization, review, idempotency and audit history.
- **No measured business outcome.** Time savings, resolution speed, activation rate and customer satisfaction are hypotheses for a future study.

## Handling customer text

Customer and sales messages are evidence data. Their contents cannot grant permissions or override tool rules. The server does not execute text, visit customer URLs or expose a shell. The bundled injection case verifies deterministic behavior only; it is not proof that every MCP host resists prompt injection.

## Before a real pilot

Use separately authorized, appropriately redacted data. Define access control, data retention, consent, evidence freshness and conflict handling. Evaluate against independently authored cases and human review. Keep a clear separation between draft creation and actual sending. These are future requirements, not claims of implemented production controls.
