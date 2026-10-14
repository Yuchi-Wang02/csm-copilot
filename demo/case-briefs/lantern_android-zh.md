# CSM Copilot — Platform review brief

> Independent portfolio prototype. All customer records are synthetic. Nothing was sent or submitted.

Snapshot: **2026-10-14T09:00:00\+00:00**
Execution: deterministic workflow replay; no model inference.
Client draft language: Chinese.

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
**Next action:** 复核并发送证据请求，收到新记录后重新评估。

| Check | State | Source record IDs |
|---|---|---|
| Platform currency approval | unknown | No applicable record |
| Production visibility setting | unknown | No applicable record |
| Placement and content | met | lantern\_android\_placement\_linked |
| SDK connection sequence | met | lantern\_android\_sdk\_connected |
| Non-test device verification | not\_met | lantern\_android\_device\_verified |
| Reward callback verification | unknown | No applicable record |

**Timing of supporting records** (oldest first)

| Record | Source type | Recorded at | Days before snapshot | Supports |
|---|---|---|---:|---|
| lantern\_android\_device\_verified | test\_record | 2026-10-09T09:00:00Z | 5.00 | device\_verified |
| lantern\_android\_placement\_linked | test\_record | 2026-10-09T09:00:00Z | 5.00 | placement\_linked |
| lantern\_android\_sdk\_connected | test\_record | 2026-10-09T09:00:00Z | 5.00 | sdk\_connected |

Age is elapsed time at the fixed snapshot, rounded to two decimals. It does not expire evidence, change readiness or prove that a report is still current. Review whether a fresh confirmation or test is needed.

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

**Request missing intake details**

- Share the SDK version used in the affected app build.
- Share the observation start and end time, including date and timezone.
- Share relevant logs with credentials, tokens, personal data and other secrets removed.

Based on the five structured intake fields for this issue \(project policy\). Recorded values are not verified; review their content and the original report before asking. Details mentioned only in free text are not extracted automatically. Additional candidate-specific evidence may still be needed.

**Original issue record**

Source type: Customer report. Recorded at: 2026-10-09T09:00:00Z.

> 我们在新加坡测试：测试机能看到广告，Android 正式设备打开奖励页面的 Offerwall 是空白的。iOS 测试正常。我们想下周五上线。

Source record: msg\_issue\_blank

**Questions to review before handoff**

Suggested questions from lexical triage. Review what is already known before asking the customer; these do not establish a root cause.

**Candidate: no offers**

- Confirm the affected app and platform.
- Share currency approval and Test Only settings for that platform.
- Compare a test device with a non-test device; include region and time.

Related documentation: https://docs.unity.com/en-us/grow/offerwall/monetization/other/faq


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
