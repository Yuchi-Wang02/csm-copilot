# Repair one callback-health denial without erasing the failure

[Open the original message and current result](https://yuchi-wang02.github.io/csm-copilot/?probe=not_failing#triage-review) · [Frozen pre-change cases](../evidence/callback-health-before.json) · [Current replay](../evidence/callback-health-review.json)

The customer asks: “Callbacks are not failing. Please explain invoicing.” Before this change, the lexical baseline returned `reward_callback`, requested callback logs and chose `collect_evidence`. It now returns `unknown` with `clarify_scope`. The CSM should clarify the invoice request; the tool does not establish a billing defect, assign Finance, verify callback health or approve launch.

## Observed failure, then a bounded rule

Twelve authored development messages were captured against commit `063583e9704af1a2583aac9ea229703510926d42` before the rule changed. Seven regression checks failed against that implementation: five message cases and two handoff variants with complete or incomplete generic fields. All fourteen focused checks pass after the repair.

The added pattern recognizes `callback` or `callbacks`, optionally preceded by `reward`, followed by present-tense `is/are not failing` or `isn't/aren't failing`. It requires a statement ending or boundary immediately afterward: a period, exclamation mark, semicolon, newline or end of text, allowing horizontal whitespace. It does not consume a question mark, qualifier, comma or closing quote. Only signal occurrences inside the matched denial are excluded; other occurrences remain eligible.

| Authored example | Current result | Reason |
|---|---|---|
| Callbacks are not failing. Please explain invoicing. | `unknown` / `clarify_scope` | The callback mention is explicitly denied in the supported form |
| Callbacks aren't failing. | `unknown` / `clarify_scope` | Present-tense contraction is included |
| Callbacks are not failing. The offerwall is blank. | `no_offers` | A separate positive Offerwall symptom remains |
| Callbacks are not failing. A later callback returned HTTP 405. | `reward_callback` | A separate callback mention remains eligible; root cause stays unconfirmed |
| Callbacks are not failing consistently. | `reward_callback` | The qualifier prevents this narrow exclusion |
| Callbacks are not failing? | `reward_callback` | A question is not treated as the supported assertion |
| Callbacks were not failing yesterday. | `reward_callback` | This extension does not infer current health from a past-tense statement |
| Search for 'callbacks are not failing' in the documentation. | `reward_callback`, still a mismatch | Quoted-topic understanding remains outside this repair |

The quoted-topic case stays visible with its authored expected category of `unknown`. The retained qualified and past-tense examples describe conservative project behavior, not an independently established semantic truth for every context. The rule does not solve reported speech, temporal reasoning, arbitrary negation or multilingual interpretation.

## Preserve what was learned

The original sixteen-case callback-denial fixture is unchanged. Its `not_failing` record still contains the pre-change output and original known-limit label. The generated replay retains that original label separately and now marks the current result as a repair. Across that older set, eight category outputs differ from the frozen baseline and two authored mismatches remain.

The fifth practice decision continues to show the **recorded before-repair result**, clearly labeled as historical. Its evidence link shows both the preserved failure and the current result. This lets someone explain the judgment they would have applied to the old recommendation and inspect how the implementation changed afterward.

The original thirty-message diagnostic remains 16/18 on reused evaluation cases after earlier adaptation. This repair does not improve that number. No new model inference or independent human validation was performed, and no customer outcomes were measured.

## Reproduce

```sh
python evaluation/callback_health.py
python evaluation/callback_denial.py
python -m pytest tests/test_callback_health.py tests/test_callback_denial.py -q
python scripts/build_demo.py
```

The frozen file contains each original tool result. The current report includes the frozen file hash, source commit and new results. Handoff tests also check that the CSM clarification route takes precedence over generic field completeness, the cause remains unconfirmed, nothing is sent and source records are not mutated.
