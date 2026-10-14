# CSM Copilot — Platform review brief

> Independent portfolio prototype. All customer records are synthetic. Nothing was sent or submitted.

Snapshot: **2026-10-14T09:00:00\+00:00**
Execution: deterministic workflow replay; no model inference.
Client draft language: English.

Scope: **harbor\_android**. Original snapshot only; the separate synthetic-update comparison is excluded. Other platforms and accounts are excluded; account contact records are retained.

## Selected platform

Selection: strictly more than three days since actual contact; missing contact history is included as unknown. Live accounts are excluded from this bundled morning queue.

| Account | Days since contact | Planned launch | Included integrations |
|---|---:|---|---|
| Harbor Studio (acc\_006) | 4.0 | 2026-10-19T09:00:00Z | 1 |

Priority is the planned launch date, not a predicted risk or revenue score. All next steps are proposals for CSM review; no deadline or customer agreement is inferred.

## Harbor Studio — acc\_006

Recorded stage: integration. Last actual contact: 2026-10-10T09:00:00\+00:00.

### Pocket Harbor / Android

**Scoped readiness:** blocked.
**Follow-up purpose:** Collect evidence. **Proposed owner:** CSM.
**Next action:** Review and send the evidence request, then reassess when new records arrive.

| Check | State | Source record IDs |
|---|---|---|
| Platform currency approval | met | harbor\_android\_currency\_approved |
| Production visibility setting | met | harbor\_android\_test\_only\_off |
| Placement and content | met | harbor\_android\_placement\_linked |
| SDK connection sequence | met | harbor\_android\_sdk\_connected |
| Non-test device verification | met | harbor\_android\_device\_verified |
| Reward callback verification | not\_met | harbor\_android\_callback\_verified |

**Timing of supporting records** (oldest first)

| Record | Source type | Recorded at | Days before snapshot | Supports |
|---|---|---|---:|---|
| harbor\_android\_callback\_verified | test\_record | 2026-10-10T09:00:00Z | 4.00 | callback\_verified |
| harbor\_android\_currency\_approved | test\_record | 2026-10-10T09:00:00Z | 4.00 | currency\_approved |
| harbor\_android\_device\_verified | test\_record | 2026-10-10T09:00:00Z | 4.00 | device\_verified |
| harbor\_android\_placement\_linked | test\_record | 2026-10-10T09:00:00Z | 4.00 | placement\_linked |
| harbor\_android\_sdk\_connected | test\_record | 2026-10-10T09:00:00Z | 4.00 | sdk\_connected |
| harbor\_android\_test\_only\_off | test\_record | 2026-10-10T09:00:00Z | 4.00 | test\_only\_off |

Age is elapsed time at the fixed snapshot, rounded to two decimals. It does not expire evidence, change readiness or prove that a report is still current. Review whether a fresh confirmation or test is needed.

A scoped evidence checklist, not a Unity launch approval or a fill guarantee.

**Customer follow-up draft — not sent**

> Hi Harbor Studio team,
> Following up on Pocket Harbor \(Android\). Our current records still need the following evidence:
> - Share a redacted callback example with HTTP status and time.
> I can consolidate your updates for technical review. Please let us know when you expect to share them.
> Launch timing remains subject to verification; this message does not confirm approval or ad availability.

Draft evidence: harbor\_android\_callback\_verified, harbor\_android\_currency\_approved, harbor\_android\_device\_verified, harbor\_android\_placement\_linked, harbor\_android\_sdk\_connected, harbor\_android\_test\_only\_off, msg\_issue\_callback. Contact history unchanged.

### Technical handoff — ticket-issue\_callback

**\[Android\] Reward callback returns HTTP 405.**

Handoff state: needs\_information. Root cause: unconfirmed.
Suggested owner: Technical support after CSM evidence review \(project policy\).

| Known field | Value | Source record |
|---|---|---|
| app | Pocket Harbor | harbor\_android |
| platform | Android | harbor\_android |
| sdk\_version | synthetic-version-1 | msg\_issue\_callback |
| region | Japan | msg\_issue\_callback |
| time\_window | 2026-10-10 08:30–09:00 UTC | msg\_issue\_callback |

**Missing information:** reproduction\_steps, redacted\_logs

**Next action:** Request missing evidence, then review the handoff; no ticket was submitted.

**Request missing intake details**

- Share the steps to reproduce the issue, including the expected and observed result.
- Share relevant logs with credentials, tokens, personal data and other secrets removed.

Based on the five structured intake fields for this issue \(project policy\). Recorded values are not verified; review their content and the original report before asking. Details mentioned only in free text are not extracted automatically. Additional candidate-specific evidence may still be needed.

**Original issue record**

Source type: Customer report. Recorded at: 2026-10-10T09:00:00Z.

> Our self-managed reward endpoint returns HTTP 405. The reward has not reached the test user. Test region: Japan. SDK: synthetic-version-1. Observed between 08:30 and 09:00 UTC on 2026-10-10.

Source record: msg\_issue\_callback

**Questions to review before handoff**

Suggested questions from lexical triage. Review what is already known before asking the customer; these do not establish a root cause.

**Candidate: reward callback**

- Which currency mode is configured?
- Share the callback time window, HTTP status and redacted logs.
- Provide a redacted transaction example and endpoint method.

Related documentation: https://docs.unity.com/en-us/grow/offerwall/monetization/virtual-currency/troubleshoot-callback-failures

HTTP 405 makes an endpoint method mismatch worth checking; it is not a confirmed cause.

## Evidence index

These are declared synthetic source records, not independent verification. Structured claims must match account, integration and checklist scope.

| Record | Account / integration | Recorded at | Source text |
|---|---|---|---|
| contact\_acc\_006 | acc\_006 / account contact | 2026-10-10T09:00:00Z | Synthetic CSM contact: received onboarding progress update. |
| harbor\_android\_callback\_verified | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Synthetic Android test record: Reward callback verification = not\_met. |
| harbor\_android\_currency\_approved | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Synthetic Android test record: Platform currency approval = met. |
| harbor\_android\_device\_verified | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Synthetic Android test record: Non-test device verification = met. |
| harbor\_android\_placement\_linked | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Synthetic Android test record: Placement and content = met. |
| harbor\_android\_sdk\_connected | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Synthetic Android test record: SDK connection sequence = met. |
| harbor\_android\_test\_only\_off | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Synthetic Android test record: Production visibility setting = met. |
| msg\_issue\_callback | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Our self-managed reward endpoint returns HTTP 405. The reward has not reached the test user. Test region: Japan. SDK: synthetic-version-1. Observed between 08:30 and 09:00 UTC on 2026-10-10. |

## Integration record index

App and platform handoff fields cite these synthetic configuration records. No per-field observation date is recorded; the export uses the bundled snapshot. These values are not independently verified and do not establish current configuration or launch approval.

| Record | Account | App | Platform |
|---|---|---|---|
| harbor\_android | acc\_006 | Pocket Harbor | Android |

## Product sources and review boundaries

- https://docs.unity.com/en-us/grow/offerwall/monetization/other/faq
- https://docs.unity.com/en-us/grow/offerwall/monetization/virtual-currency/troubleshoot-callback-failures

The rule register distinguishes official product documentation from project operating policies. Checklist completion is not vendor launch approval. Triage candidates are not confirmed root causes. Promise-pattern lint does not verify arbitrary model-written claims.

This export is a deterministic review artifact, not evidence of a live model run, independent human validation, customer impact or actual outreach.
