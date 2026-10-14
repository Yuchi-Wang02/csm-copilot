# CSM Copilot — Morning review brief

> Independent portfolio prototype. All customer records are synthetic. Nothing was sent or submitted.

Snapshot: **2026-10-14T09:00:00\+00:00**
Execution: deterministic workflow replay; no model inference.
Client draft language: Chinese.

## Today's review queue

Selection: strictly more than three days since actual contact; missing contact history is included as unknown. Live accounts are excluded from this bundled morning queue.

| Account | Days since contact | Planned launch | Integrations |
|---|---:|---|---|
| Lantern Games (acc\_014) | 5.0 | 2026-10-16T09:00:00Z | 2 |
| Meadow Works (acc\_018) | 5.0 | 2026-10-18T09:00:00Z | 1 |
| Harbor Studio (acc\_006) | 4.0 | 2026-10-19T09:00:00Z | 1 |

Priority is the planned launch date, not a predicted risk or revenue score. All next steps are proposals for CSM review; no deadline or customer agreement is inferred.

## Lantern Games — acc\_014

Recorded stage: validation. Last actual contact: 2026-10-09T09:00:00\+00:00.

### Moon Garden / Android

**Scoped readiness:** blocked.
**Follow-up purpose:** Collect evidence. **Proposed owner:** CSM.
**Next action:** 复核并发送证据请求，收到新记录后重新评估。

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

> Lantern Games 团队好，
> 跟进 Moon Garden（Android）的接入进展，目前记录还需要以下证据：
> - 请确认该平台的虚拟货币审批状态。
> - 请确认正式内容是否关闭 Test Only。
> - 请提供非测试设备的最新验证，注明地区、时间和观察结果。
> - 请提供脱敏回调样例，注明 HTTP 状态和时间。
> 收到后我可以汇总信息交给技术同事复核，请告知预计何时可以提供。
> 上线时间仍需核验；本消息不代表审核通过或广告供应承诺。

Draft evidence: lantern\_android\_device\_verified, lantern\_android\_placement\_linked, lantern\_android\_sdk\_connected, msg\_issue\_blank. Contact history unchanged.

### Moon Garden / iOS

**Scoped readiness:** checklist\_complete.
**Follow-up purpose:** Review the launch plan. **Proposed owner:** CSM.
**Next action:** 复核上线计划，并确认上次检查后是否有变更。

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

> Lantern Games 团队好，
> 根据现有记录，Moon Garden（iOS）已完成本项目范围内的检查清单。
> 请确认上次检查后是否有变更，以及拟定的上线计划是否仍适用。之后我们可以一起复核其余上线决策。
> 上线时间仍需核验；本消息不代表审核通过或广告供应承诺。

Draft evidence: lantern\_ios\_callback\_verified, lantern\_ios\_currency\_approved, lantern\_ios\_device\_verified, lantern\_ios\_placement\_linked, lantern\_ios\_sdk\_connected, lantern\_ios\_test\_only\_off. Contact history unchanged.

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

## Meadow Works — acc\_018

Recorded stage: validation. Last actual contact: 2026-10-09T09:00:00\+00:00.

### Meadow Notes / iOS

**Scoped readiness:** needs\_evidence.
**Follow-up purpose:** Collect evidence. **Proposed owner:** CSM.
**Next action:** 复核并发送证据请求，收到新记录后重新评估。

| Check | State | Source record IDs |
|---|---|---|
| Platform currency approval | met | meadow\_ios\_currency\_approved |
| Production visibility setting | met | meadow\_ios\_test\_only\_off |
| Placement and content | met | meadow\_ios\_placement\_linked |
| SDK connection sequence | met | meadow\_ios\_sdk\_connected |
| Non-test device verification | unknown | No applicable record |
| Reward callback verification | not\_applicable | No applicable record |

A scoped evidence checklist, not a Unity launch approval or a fill guarantee.

**Customer follow-up draft — not sent**

> Meadow Works 团队好，
> 跟进 Meadow Notes（iOS）的接入进展，目前记录还需要以下证据：
> - 请提供非测试设备的最新验证，注明地区、时间和观察结果。
> 收到后我可以汇总信息交给技术同事复核，请告知预计何时可以提供。
> 上线时间仍需核验；本消息不代表审核通过或广告供应承诺。

Draft evidence: meadow\_ios\_currency\_approved, meadow\_ios\_placement\_linked, meadow\_ios\_sdk\_connected, meadow\_ios\_test\_only\_off. Contact history unchanged.

## Harbor Studio — acc\_006

Recorded stage: integration. Last actual contact: 2026-10-10T09:00:00\+00:00.

### Pocket Harbor / Android

**Scoped readiness:** blocked.
**Follow-up purpose:** Collect evidence. **Proposed owner:** CSM.
**Next action:** 复核并发送证据请求，收到新记录后重新评估。

| Check | State | Source record IDs |
|---|---|---|
| Platform currency approval | met | harbor\_android\_currency\_approved |
| Production visibility setting | met | harbor\_android\_test\_only\_off |
| Placement and content | met | harbor\_android\_placement\_linked |
| SDK connection sequence | met | harbor\_android\_sdk\_connected |
| Non-test device verification | met | harbor\_android\_device\_verified |
| Reward callback verification | not\_met | harbor\_android\_callback\_verified |

A scoped evidence checklist, not a Unity launch approval or a fill guarantee.

**Customer follow-up draft — not sent**

> Harbor Studio 团队好，
> 跟进 Pocket Harbor（Android）的接入进展，目前记录还需要以下证据：
> - 请提供脱敏回调样例，注明 HTTP 状态和时间。
> 收到后我可以汇总信息交给技术同事复核，请告知预计何时可以提供。
> 上线时间仍需核验；本消息不代表审核通过或广告供应承诺。

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

## Evidence index

These are declared synthetic source records, not independent verification. Structured claims must match account, integration and checklist scope.

| Record | Account / integration | Recorded at | Source text |
|---|---|---|---|
| contact\_acc\_014 | acc\_014 / account contact | 2026-10-09T09:00:00Z | Synthetic CSM contact: received onboarding progress update. |
| lantern\_android\_device\_verified | acc\_014 / lantern\_android | 2026-10-09T09:00:00Z | Synthetic Android test record: Non-test device verification = not\_met. |
| lantern\_android\_placement\_linked | acc\_014 / lantern\_android | 2026-10-09T09:00:00Z | Synthetic Android test record: Placement and content = met. |
| lantern\_android\_sdk\_connected | acc\_014 / lantern\_android | 2026-10-09T09:00:00Z | Synthetic Android test record: SDK connection sequence = met. |
| lantern\_ios\_callback\_verified | acc\_014 / lantern\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Reward callback verification = met. |
| lantern\_ios\_currency\_approved | acc\_014 / lantern\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Platform currency approval = met. |
| lantern\_ios\_device\_verified | acc\_014 / lantern\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Non-test device verification = met. |
| lantern\_ios\_placement\_linked | acc\_014 / lantern\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Placement and content = met. |
| lantern\_ios\_sdk\_connected | acc\_014 / lantern\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: SDK connection sequence = met. |
| lantern\_ios\_test\_only\_off | acc\_014 / lantern\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Production visibility setting = met. |
| msg\_issue\_blank | acc\_014 / lantern\_android | 2026-10-09T09:00:00Z | 我们在新加坡测试：测试机能看到广告，Android 正式设备打开奖励页面的 Offerwall 是空白的。iOS 测试正常。我们想下周五上线。 |
| contact\_acc\_018 | acc\_018 / account contact | 2026-10-09T09:00:00Z | Synthetic CSM contact: received onboarding progress update. |
| meadow\_ios\_currency\_approved | acc\_018 / meadow\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Platform currency approval = met. |
| meadow\_ios\_placement\_linked | acc\_018 / meadow\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Placement and content = met. |
| meadow\_ios\_sdk\_connected | acc\_018 / meadow\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: SDK connection sequence = met. |
| meadow\_ios\_test\_only\_off | acc\_018 / meadow\_ios | 2026-10-09T09:00:00Z | Synthetic iOS test record: Production visibility setting = met. |
| contact\_acc\_006 | acc\_006 / account contact | 2026-10-10T09:00:00Z | Synthetic CSM contact: received onboarding progress update. |
| harbor\_android\_callback\_verified | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Synthetic Android test record: Reward callback verification = not\_met. |
| harbor\_android\_currency\_approved | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Synthetic Android test record: Platform currency approval = met. |
| harbor\_android\_device\_verified | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Synthetic Android test record: Non-test device verification = met. |
| harbor\_android\_placement\_linked | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Synthetic Android test record: Placement and content = met. |
| harbor\_android\_sdk\_connected | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Synthetic Android test record: SDK connection sequence = met. |
| harbor\_android\_test\_only\_off | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Synthetic Android test record: Production visibility setting = met. |
| msg\_issue\_callback | acc\_006 / harbor\_android | 2026-10-10T09:00:00Z | Our self-managed reward endpoint returns HTTP 405. The reward has not reached the test user. Test region: Japan. SDK: synthetic-version-1. Observed between 08:30 and 09:00 UTC on 2026-10-10. |

## Product sources and review boundaries

- https://docs.unity.com/en-us/grow/offerwall/monetization/other/faq
- https://docs.unity.com/en-us/grow/offerwall/monetization/virtual-currency/troubleshoot-callback-failures

The rule register distinguishes official product documentation from project operating policies. Checklist completion is not vendor launch approval. Triage candidates are not confirmed root causes. Promise-pattern lint does not verify arbitrary model-written claims.

This export is a deterministic review artifact, not evidence of a live model run, independent human validation, customer impact or actual outreach.
