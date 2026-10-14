# CSM Copilot — Platform review brief

> Independent portfolio prototype. All customer records are synthetic. Nothing was sent or submitted.

Snapshot: **2026-10-14T09:00:00\+00:00**
Execution: deterministic workflow replay; no model inference.
Client draft language: English.

Scope: **meadow\_ios**. Original snapshot only; the separate synthetic-update comparison is excluded. Other platforms and accounts are excluded; account contact records are retained.

## Selected platform

Selection: strictly more than three days since actual contact; missing contact history is included as unknown. Live accounts are excluded from this bundled morning queue.

| Account | Days since contact | Planned launch | Included integrations |
|---|---:|---|---|
| Meadow Works (acc\_018) | 5.0 | 2026-10-18T09:00:00Z | 1 |

Priority is the planned launch date, not a predicted risk or revenue score. All next steps are proposals for CSM review; no deadline or customer agreement is inferred.

## Meadow Works — acc\_018

Recorded stage: validation. Last actual contact: 2026-10-09T09:00:00\+00:00.

### Meadow Notes / iOS

**Scoped readiness:** needs\_evidence.
**Follow-up purpose:** Collect evidence. **Proposed owner:** CSM.
**Next action:** Review and send the evidence request, then reassess when new records arrive.

| Check | State | Source record IDs |
|---|---|---|
| Platform currency approval | met | meadow\_ios\_currency\_approved |
| Production visibility setting | met | meadow\_ios\_test\_only\_off |
| Placement and content | met | meadow\_ios\_placement\_linked |
| SDK connection sequence | met | meadow\_ios\_sdk\_connected |
| Non-test device verification | unknown | No applicable record |
| Reward callback verification | not\_applicable | No applicable record |

**Timing of supporting records** (oldest first)

| Record | Source type | Recorded at | Days before snapshot | Supports |
|---|---|---|---:|---|
| meadow\_ios\_currency\_approved | test\_record | 2026-10-09T09:00:00Z | 5.00 | currency\_approved |
| meadow\_ios\_placement\_linked | test\_record | 2026-10-09T09:00:00Z | 5.00 | placement\_linked |
| meadow\_ios\_sdk\_connected | test\_record | 2026-10-09T09:00:00Z | 5.00 | sdk\_connected |
| meadow\_ios\_test\_only\_off | test\_record | 2026-10-09T09:00:00Z | 5.00 | test\_only\_off |

Age is elapsed time at the fixed snapshot, rounded to two decimals. It does not expire evidence, change readiness or prove that a report is still current. Review whether a fresh confirmation or test is needed.

A scoped evidence checklist, not a Unity launch approval or a fill guarantee.

**Customer follow-up draft — not sent**

> Hi Meadow Works team,
> Following up on Meadow Notes \(iOS\). Our current records still need the following evidence:
> - Share a fresh non-test-device check with region, time and observed result.
> I can consolidate your updates for technical review. Please let us know when you expect to share them.
> Launch timing remains subject to verification; this message does not confirm approval or ad availability.

Draft evidence: meadow\_ios\_currency\_approved, meadow\_ios\_placement\_linked, meadow\_ios\_sdk\_connected, meadow\_ios\_test\_only\_off. Contact history unchanged.

**Recorded issues:** None for this platform in the snapshot. This does not establish that no issue exists or that a previous issue was resolved.

## Evidence index

These are declared synthetic source records, not independent verification. Structured claims must match account, integration and checklist scope.

| Record | Account / integration | Recorded at | Source text |
|---|---|---|---|
| contact\_acc\_018 | acc\_018 / account contact | 2026-10-09T09:00:00Z | Synthetic CSM contact: received onboarding progress update. |
| meadow\_ios\_currency\_approved | acc\_018 / meadow\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Platform currency approval = met. |
| meadow\_ios\_placement\_linked | acc\_018 / meadow\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Placement and content = met. |
| meadow\_ios\_sdk\_connected | acc\_018 / meadow\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: SDK connection sequence = met. |
| meadow\_ios\_test\_only\_off | acc\_018 / meadow\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Production visibility setting = met. |

## Product sources and review boundaries

- https://docs.unity.com/en-us/grow/offerwall/monetization/other/faq
- https://docs.unity.com/en-us/grow/offerwall/monetization/virtual-currency/troubleshoot-callback-failures

The rule register distinguishes official product documentation from project operating policies. Checklist completion is not vendor launch approval. Triage candidates are not confirmed root causes. Promise-pattern lint does not verify arbitrary model-written claims.

This export is a deterministic review artifact, not evidence of a live model run, independent human validation, customer impact or actual outreach.
