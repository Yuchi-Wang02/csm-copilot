# CSM Copilot — Platform review brief

> Independent portfolio prototype. All customer records are synthetic. Nothing was sent or submitted.

Snapshot: **2026-10-14T09:00:00\+00:00**
Execution: deterministic workflow replay; no model inference.
Client draft language: English.

Scope: **lantern\_ios**. Original snapshot only; the separate synthetic-update comparison is excluded. Other platforms and accounts are excluded; account contact records are retained.

## Selected platform

Selection: strictly more than three days since actual contact; missing contact history is included as unknown. Live accounts are excluded from this bundled morning queue.

| Account | Days since contact | Planned launch | Included integrations |
|---|---:|---|---|
| Lantern Games (acc\_014) | 5.0 | 2026-10-16T09:00:00Z | 1 |

Priority is the planned launch date, not a predicted risk or revenue score. All next steps are proposals for CSM review; no deadline or customer agreement is inferred.

## Lantern Games — acc\_014

Recorded stage: validation. Last actual contact: 2026-10-09T09:00:00\+00:00.

### Moon Garden / iOS

**Scoped readiness:** checklist\_complete.
**Follow-up purpose:** Review the launch plan. **Proposed owner:** CSM.
**Next action:** Review the launch plan and confirm any changes since the recorded checks.

| Check | State | Source record IDs |
|---|---|---|
| Platform currency approval | met | lantern\_ios\_currency\_approved |
| Production visibility setting | met | lantern\_ios\_test\_only\_off |
| Placement and content | met | lantern\_ios\_placement\_linked |
| SDK connection sequence | met | lantern\_ios\_sdk\_connected |
| Non-test device verification | met | lantern\_ios\_device\_verified |
| Reward callback verification | met | lantern\_ios\_callback\_verified |

A scoped evidence checklist, not a Unity launch approval or a fill guarantee.

**Customer follow-up draft — not sent**

> Hi Lantern Games team,
> Our scoped checklist for Moon Garden \(iOS\) is complete based on the recorded evidence.
> Please confirm whether anything has changed since those checks and whether the proposed launch plan is still current. We can then review the remaining launch decisions together.
> Launch timing remains subject to verification; this message does not confirm approval or ad availability.

Draft evidence: lantern\_ios\_callback\_verified, lantern\_ios\_currency\_approved, lantern\_ios\_device\_verified, lantern\_ios\_placement\_linked, lantern\_ios\_sdk\_connected, lantern\_ios\_test\_only\_off. Contact history unchanged.

**Recorded issues:** None for this platform in the snapshot. This does not establish that no issue exists or that a previous issue was resolved.

## Evidence index

These are declared synthetic source records, not independent verification. Structured claims must match account, integration and checklist scope.

| Record | Account / integration | Recorded at | Source text |
|---|---|---|---|
| contact\_acc\_014 | acc\_014 / account contact | 2026-10-09T09:00:00Z | Synthetic CSM contact: received onboarding progress update. |
| lantern\_ios\_callback\_verified | acc\_014 / lantern\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Reward callback verification = met. |
| lantern\_ios\_currency\_approved | acc\_014 / lantern\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Platform currency approval = met. |
| lantern\_ios\_device\_verified | acc\_014 / lantern\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Non-test device verification = met. |
| lantern\_ios\_placement\_linked | acc\_014 / lantern\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Placement and content = met. |
| lantern\_ios\_sdk\_connected | acc\_014 / lantern\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: SDK connection sequence = met. |
| lantern\_ios\_test\_only\_off | acc\_014 / lantern\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Production visibility setting = met. |

## Product sources and review boundaries

- https://docs.unity.com/en-us/grow/offerwall/monetization/other/faq
- https://docs.unity.com/en-us/grow/offerwall/monetization/virtual-currency/troubleshoot-callback-failures

The rule register distinguishes official product documentation from project operating policies. Checklist completion is not vendor launch approval. Triage candidates are not confirmed root causes. Promise-pattern lint does not verify arbitrary model-written claims.

This export is a deterministic review artifact, not evidence of a live model run, independent human validation, customer impact or actual outreach.
