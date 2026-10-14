# CSM Copilot — Platform review brief

> Independent portfolio prototype. All customer records are synthetic. Nothing was sent or submitted.

Snapshot: **2026-10-14T09:00:00\+00:00**
Execution: deterministic workflow replay; no model inference.
Client draft language: English.

Scope: **lantern\_android**. Original snapshot only; the separate synthetic-update comparison is excluded. Other platforms and accounts are excluded; account contact records are retained.

## Selected platform

Selection: strictly more than three days since actual contact; missing contact history is included as unknown. Live accounts are excluded from this bundled morning queue.

| Account | Days since contact | Planned launch | Included integrations |
|---|---:|---|---|
| Lantern Games (acc\_014) | 5.0 | 2026-10-16T09:00:00Z | 1 |

Priority is the planned launch date, not a predicted risk or revenue score. All next steps are proposals for CSM review; no deadline or customer agreement is inferred.

## Lantern Games — acc\_014

Recorded stage: validation. Last actual contact: 2026-10-09T09:00:00\+00:00.

### Moon Garden / Android

**Scoped readiness:** blocked.
**Follow-up purpose:** Collect evidence. **Proposed owner:** CSM.
**Next action:** Review and send the evidence request, then reassess when new records arrive.

| Check | State | Source record IDs |
|---|---|---|
| Platform currency approval | unknown | No applicable record |
| Production visibility setting | unknown | No applicable record |
| Placement and content | met | lantern\_android\_placement\_linked |
| SDK connection sequence | met | lantern\_android\_sdk\_connected |
| Non-test device verification | not\_met | lantern\_android\_device\_verified |
| Reward callback verification | unknown | No applicable record |

A scoped evidence checklist, not a Unity launch approval or a fill guarantee.

**Customer follow-up draft — not sent**

> Hi Lantern Games team,
> Following up on Moon Garden \(Android\). Our current records still need the following evidence:
> - Confirm currency approval for this platform.
> - Confirm whether Test Only is disabled for the production content.
> - Share a fresh non-test-device check with region, time and observed result.
> - Share a redacted callback example with HTTP status and time.
> I can consolidate your updates for technical review. Please let us know when you expect to share them.
> Launch timing remains subject to verification; this message does not confirm approval or ad availability.

Draft evidence: lantern\_android\_device\_verified, lantern\_android\_placement\_linked, lantern\_android\_sdk\_connected, msg\_issue\_blank. Contact history unchanged.

### Technical handoff — ticket-issue\_blank

**\[Android\] Test device shows offers; non-test Android device has a blank offerwall.**

Handoff state: needs\_information. Root cause: unconfirmed.
Suggested owner: Technical support after CSM evidence review \(project policy\).

| Known field | Value | Source record |
|---|---|---|
| app | Moon Garden | lantern\_android |
| platform | Android | lantern\_android |
| region | Singapore | msg\_issue\_blank |
| reproduction\_steps | Open the reward screen on a non-test Android device. | msg\_issue\_blank |

**Missing information:** sdk\_version, time\_window, redacted\_logs

**Next action:** Request missing evidence, then review the handoff; no ticket was submitted.

## Evidence index

These are declared synthetic source records, not independent verification. Structured claims must match account, integration and checklist scope.

| Record | Account / integration | Recorded at | Source text |
|---|---|---|---|
| contact\_acc\_014 | acc\_014 / account contact | 2026-10-09T09:00:00Z | Synthetic CSM contact: received onboarding progress update. |
| lantern\_android\_device\_verified | acc\_014 / lantern\_android | 2026-10-09T09:00:00Z | Synthetic Android test record: Non-test device verification = not\_met. |
| lantern\_android\_placement\_linked | acc\_014 / lantern\_android | 2026-10-09T09:00:00Z | Synthetic Android test record: Placement and content = met. |
| lantern\_android\_sdk\_connected | acc\_014 / lantern\_android | 2026-10-09T09:00:00Z | Synthetic Android test record: SDK connection sequence = met. |
| msg\_issue\_blank | acc\_014 / lantern\_android | 2026-10-09T09:00:00Z | 我们在新加坡测试：测试机能看到广告，Android 正式设备打开奖励页面的 Offerwall 是空白的。iOS 测试正常。我们想下周五上线。 |

## Product sources and review boundaries

- https://docs.unity.com/en-us/grow/offerwall/monetization/other/faq
- https://docs.unity.com/en-us/grow/offerwall/monetization/virtual-currency/troubleshoot-callback-failures

The rule register distinguishes official product documentation from project operating policies. Checklist completion is not vendor launch approval. Triage candidates are not confirmed root causes. Promise-pattern lint does not verify arbitrary model-written claims.

This export is a deterministic review artifact, not evidence of a live model run, independent human validation, customer impact or actual outreach.
