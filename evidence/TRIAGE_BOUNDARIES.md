# Triage phrase-boundary repair

AI-assisted development probes authored for this repair, including two known failures reused from the original diagnostic set. Not an independent test or a general accuracy estimate.

## What changed

The earlier lexical pattern matched `blank` inside `blanket`, `no offers` inside `casino offers`, and `no ads` inside `no adservers`. An unrelated invoice request could therefore receive Offerwall checks and a proposed technical handoff.

The English no-offers phrases now have Latin-letter boundaries. Common forms such as blanking and empty offerwalls remain supported, and Chinese characters can sit directly beside an English signal. Reward/callback retrieval is unchanged. A later explicit-denial check also excludes selected English and Chinese no-offers mentions; see the negation review. These are bounded lexical repairs, not semantic classification or a general tokenizer.

[Pre-change code](https://github.com/Yuchi-Wang02/csm-copilot/blob/a3ddd2997b014830b5da5ef7fbedae0977735a05/src/csm_copilot/engine.py) · [Recorded pre-change engine outputs](triage-boundary-before.json) · [Current outputs](triage-boundary-review.json)

## Paired observations

| Probe | Customer message | Expected | Before | After |
|---|---|---|---|---|
| blanket\_invoice | Please send the blanket invoice for our annual plan. | unknown | no\_offers | unknown |
| casino\_offers | Our casino offers an annual plan; how do we change billing? | unknown | no\_offers | unknown |
| adserver\_invoice | There are no adservers listed on this invoice. | unknown | no\_offers | unknown |
| mixed\_invoice | 请发一份 blanket invoice，我们需要对账。 | unknown | no\_offers | unknown |
| uppercase\_blank | The Offerwall is BLANK. | no\_offers | no\_offers | no\_offers |
| blanking | The Offerwall keeps blanking on the device. | no\_offers | no\_offers | no\_offers |
| plural\_offerwalls | We see empty offerwalls on both phones. | no\_offers | no\_offers | no\_offers |
| mixed\_blank | Android页面blank，请协助排查。 | no\_offers | no\_offers | no\_offers |
| mixed\_two\_issues | 页面空白，reward callback返回405。 | no\_offers, reward\_callback | no\_offers, reward\_callback | no\_offers, reward\_callback |
| hyphenated\_screen | We have a blank-screen issue with no ads. | no\_offers | no\_offers | no\_offers |
| negated\_symptom | No offers is not our problem. Please explain invoicing. | unknown | no\_offers | unknown |
| indirect\_inventory | The opportunity list contains zero items. | no\_offers | unknown | unknown |

Changed categories on 5 of these 12 development probes. 1 known semantic failures remain. These counts describe this selected set only.

## Workflow consequence

The blanket-invoice example now returns `clarify_scope`. A ticket based on that message stays with the CSM to clarify the problem, even when generic SDK/log fields are present. It does not classify billing or choose a Finance owner; those capabilities are outside this prototype.

Six regression checks failed before the repair and passed afterward: four substring collisions and two handoff variants with complete/incomplete generic fields. Six positive-message probes retain their expected categories. At the phrase-boundary release, both semantic failures remained. The later explicit-denial check now addresses the negated-symptom case; indirect wording still fails.

## Limits and reproduction

The original 30-message diagnostic inputs are unchanged. The original 14/18 result is preserved in `negation-before.json`. After using inspected negation failures to develop the later rule, the current replay is 16/18; indirect wording still fails. This is a reused-case result, not independent validation. The new probes were authored during this repair and are not held out. No independent human labeling, model run, customer outcome or productivity measurement was performed.
A standalone term such as blank can still describe an invoice or another unrelated object. Phrase boundaries do not determine whether the sentence reports an Offerwall problem.

```sh
python evaluation/triage_boundaries.py
python -m pytest tests/test_triage_boundaries.py -q
```

Inputs SHA-256: `ce8661580659989974d2b95e91b72f662ee99ab944e7918eb18386843ffd13bd`
