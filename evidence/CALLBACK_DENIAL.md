# Callback denial: keep the request separate from the denied symptom

AI-assisted developer-authored probes. Captured before the callback-denial change; not held out or independently labelled. No model inference.

An explicit local denial such as `the reward callback is not our problem` or `不是奖励回调的问题` should not trigger callback troubleshooting solely because it contains callback words. The matcher excludes only signal occurrences inside supported denial spans. A separate positive callback or blank-Offerwall symptom remains eligible.

The exclusion is a project lexical rule. It does not infer a billing workflow, identify a confirmed root cause, close an existing issue or send a message. Denial-only requests remain with the CSM for scope clarification, even when generic handoff fields are complete.

Frozen before commit: `b1a7ca2059a4fea529bb3c433ceb8b7e1f33db8c`. [Original outputs](callback-denial-before.json) · [Current replay](callback-denial-review.json).

| Probe | Message | Expected | Before | Current |
|---|---|---|---|---|
| callback\_denial\_en | The reward callback is not our problem. Please explain invoicing. | unknown | reward\_callback | unknown |
| callback\_contraction | Reward callbacks aren't our problem. Please explain invoicing. | unknown | reward\_callback | unknown |
| reward\_denial | Rewards are not the issue. Please explain invoicing. | unknown | reward\_callback | unknown |
| callback\_denial\_zh | 不是奖励回调的问题，请说明账单。 | unknown | reward\_callback | unknown |
| callback\_denial\_zh\_alt | 并非回调故障，请说明账单。 | unknown | reward\_callback | unknown |
| denied\_with\_blank | The reward callback is not our problem. The offerwall is blank on Android. | no\_offers | no\_offers, reward\_callback | no\_offers |
| denied\_with\_blank\_zh | 不是奖励回调的问题，广告墙空白。 | no\_offers | no\_offers, reward\_callback | no\_offers |
| separate\_callback | The iOS callback is not our problem. Android callback returns HTTP 405. | reward\_callback | reward\_callback | reward\_callback |
| separate\_callback\_zh | 不是iOS的问题；Android奖励回调失败。 | reward\_callback | reward\_callback | reward\_callback |
| not\_only | The reward callback is not our only problem. The offerwall is blank. | no\_offers, reward\_callback | no\_offers, reward\_callback | no\_offers, reward\_callback |
| cannot\_fix | We cannot fix the reward callback. | reward\_callback | reward\_callback | reward\_callback |
| positive | Reward callback returns HTTP 405. | reward\_callback | reward\_callback | reward\_callback |
| negative\_result | The reward has not arrived. | reward\_callback | reward\_callback | reward\_callback |
| qualified | The callback isn't exactly our problem. Please explain invoicing. | unknown | reward\_callback | reward\_callback |
| not\_failing | Callbacks are not failing. Please explain invoicing. | unknown | reward\_callback | reward\_callback |
| quoted | Please search for 'reward callback' in the documentation index. | unknown | reward\_callback | reward\_callback |

Seven selected messages change categories. Eleven checks failed before the repair: those seven message cases and four English/Chinese handoff variants with complete or incomplete generic fields. All twenty focused checks now pass, including assertions preserving three known failures.

Qualified denial, `callbacks are not failing`, and quoted documentation topics still produce unwanted callback candidates. The old no-offers probes also retain qualified-negation and quoted-topic failures. This does not solve negation, temporal scope, reported speech or multilingual understanding generally.

These sixteen probes were authored and inspected during development. The old twenty-probe file and original thirty-message diagnostic were not relabelled. The original diagnostic remains 16/18 after earlier adaptation; this repair does not improve that number. Historical model recordings are unchanged, with no new inference or independent human/customer validation.

```sh
python evaluation/callback_denial.py
python -m pytest tests/test_callback_denial.py -q
```
