# Explicit denial in triage: a bounded repair

Twenty AI-assisted developer-authored probes inspected while building this rule. Not held out, independently labelled or a general accuracy estimate. No model inference.

## Decision and implementation

A message explicitly denying a no-offers problem should not become a technical handoff solely because the denied phrase occurs in the text. The matcher now excludes signal occurrences contained in supported local denial patterns. It still evaluates other occurrences and callback signals separately. It does not discard an entire sentence or message after seeing `not`.

Supported forms include `no offers is not our problem`, `isn't blank`, `不是没有广告的问题`, and `页面并不空白`. Another platform's positive symptom survives, as do `not only blank` and `not our only problem`. The result notes when a denial was excluded. Root cause remains unconfirmed.

## Recorded before and after

Original code commit: `0308c77b71ede2daaf16202c383be30eb43d8bce`. [Frozen outputs and original diagnostic](negation-before.json) · [Current replay](negation-review.json).

| Probe | Message | Expected | Before | Current |
|---|---|---|---|---|
| denial\_en | No offers is not our problem. Please explain invoicing. | unknown | no\_offers | unknown |
| denial\_plural | No ads are not the issue. We need an invoice. | unknown | no\_offers | unknown |
| denial\_contraction | No offers isn't our problem. Please explain the annual plan. | unknown | no\_offers | unknown |
| negative\_blank | The offerwall is not blank. We need billing information. | unknown | no\_offers | unknown |
| negative\_blank\_contraction | The offerwall isn't blank. Please clarify invoicing. | unknown | no\_offers | unknown |
| denial\_zh | 不是没有广告的问题，请解释发票。 | unknown | no\_offers | unknown |
| denial\_zh\_alt | 并非空白的问题，请解释账单。 | unknown | no\_offers | unknown |
| negative\_blank\_zh | 页面并不空白，我们想问续费。 | unknown | no\_offers | unknown |
| denied\_plus\_callback | No offers is not our problem. The reward callback returns 405. | reward\_callback | no\_offers, reward\_callback | reward\_callback |
| denied\_plus\_callback\_zh | 不是没有广告的问题，奖励回调返回405。 | reward\_callback | no\_offers, reward\_callback | reward\_callback |
| positive\_after\_denial | No offers is not our problem on iOS. Android has no offers. | no\_offers | no\_offers | no\_offers |
| positive\_after\_denial\_zh | 不是没有广告的问题，但另一台Android没有广告。 | no\_offers | no\_offers | no\_offers |
| not\_only | The offerwall is not only blank but the reward callback also fails. | no\_offers, reward\_callback | no\_offers, reward\_callback | no\_offers, reward\_callback |
| not\_only\_problem | No offers is not our only problem. The callback fails too. | no\_offers, reward\_callback | no\_offers, reward\_callback | no\_offers, reward\_callback |
| cannot\_fix | We cannot fix the blank offerwall. | no\_offers | no\_offers | no\_offers |
| ordinary\_negative\_signal | There are no ads in this region. | no\_offers | no\_offers | no\_offers |
| ordinary\_two\_zh | 没有广告，奖励回调也失败。 | no\_offers, reward\_callback | no\_offers, reward\_callback | no\_offers, reward\_callback |
| qualified\_negation | The offerwall isn't exactly blank. We need billing information. | unknown | no\_offers | no\_offers |
| quoted\_topic | Please search for 'no offers' in the documentation index. | unknown | no\_offers | no\_offers |
| callback\_denial | The reward callback is not our problem. Please explain invoicing. | unknown | reward\_callback | unknown |

Categories change on 11 selected probes. 2 selected counterexamples still fail. Twelve regression checks failed before the repair: ten message cases and two handoff variants. The 24-check regression suite retains the frozen inputs and separate positive signals. The originally recorded callback-denial failure is now repaired by the separately documented callback rule.

## What the score cannot establish

The original 30-message diagnostic is unchanged, but its negation cases informed this rule. Its earlier 14/18 family-separated result is preserved in the frozen record. The current 16/18 is a replay after adaptation on inspected cases, not an independent improvement estimate. The remaining English and Chinese indirect-inventory cases still fail. No model run or human customer review was added by this change.

Qualified negation (`isn't exactly blank`) and quoted search topics remain counterexamples here. The [callback-denial review](CALLBACK_DENIAL.md) preserves the original callback failure, its bounded repair and three remaining callback counterexamples. Nested denial, reported speech, temporal scope and multilingual nuance require semantic review; this pattern list does not solve negation generally. A standalone `blank` may also describe something unrelated to Offerwall.

## Workflow consequence

A denied no-offers message with no other recognized symptom remains `clarify_scope`; its handoff stays `needs_scope` with the CSM even if generic logs/SDK fields are complete. A separate callback symptom remains eligible for evidence collection. No billing owner is invented and no message or ticket is sent.

```sh
python evaluation/negation.py
python -m pytest tests/test_negation.py -q
```

Inputs SHA-256: `ebffd995d485b210370680ba09e34a693979a6b8b1511a460cd6d13305c21a04`
