# Share a review, recording or triage example

The **Copy this review link** button produces a public URL that opens the selected synthetic integration, review step and client language. The comparison toggle is also preserved. The **View share link** control exposes a selectable URL if clipboard permission is unavailable.

Use these examples to start an interview at a concrete decision:

| Example | What to demonstrate |
|---|---|
| [Android evidence](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en#workspace) | Unknown settings and a recorded failed device check lead to different requests |
| [Chinese iOS follow-up](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_ios&view=followup&lang=zh#workspace) | A complete scoped checklist leads to launch-plan review, without a promise of approval |
| [Harbor's technical handoff](https://yuchi-wang02.github.io/csm-copilot/?case=harbor_android&view=handoff&lang=en#workspace) | HTTP 405 is a clue rather than a confirmed root cause; missing logs and reproduction steps remain visible |
| [Android with fresh test records](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en&update=2#customer-update) | Scoped checks complete; the draft still asks about the earlier issue |
| [Android after two confirmations](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en&update=1#customer-update) | The separate comparison changes two settings while retaining a failed device check |

## Navigation behavior

The AI trace section has its own **Copy this recording link** button and **View recording link** fallback. Its URL contains only a `run` ID from the published catalog and opens the selected attempt, task, unedited output and review. It does not include case selections or practice notes. Use these direct examples:

| Recording | Discussion point |
|---|---|
| [Four calls, unsupported explanation](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-batch#model-runs) | Tool completion does not establish evidence fidelity |
| [Structured fields after corrections](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-constrained#model-runs) | Matching fields and faithful prose are separate questions |
| [Original invoice questions](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-triage-scope#model-runs) | A correct unknown category can still produce an inappropriate follow-up |
| [Neutral scope questions](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-triage-neutral-questions#model-runs) | Inspect what changed and why customer-specific review still matters |

Selecting a recording or using the callback-comparison buttons updates the URL. Reload, Back and Forward restore that recording. Changing a case keeps an explicitly selected recording in the browser address; the separate copy buttons intentionally share only their own review or recording. Unknown, blank and repeated `run` values show the latest published attempt with a visible notice. A link with no `run` simply uses the latest attempt.

Changing the account, platform, review step, language or comparison toggle updates the browser URL. Back and Forward restore the previous selection. Direct links work on the static GitHub Pages site without a server route or login.

The iOS practice evidence link opens the iOS follow-up; the Android practice link opens the updated comparison. These links navigate within the loaded page, preserving practice notes. Opening a new tab or reloading still starts a fresh practice session.

The comparison toggle applies only to the separate counterfactual section. The account workspace always shows the original snapshot, with its original drafts and handoffs. This prevents the comparison from silently altering the evidence being reviewed.

## Share the triage learning trail

The triage explorer has a **Copy this triage link** button and a selectable **View triage link** fallback. Each link opens one published message, its preserved before-change categories, current result and project expectation.

| Example | Discussion point |
|---|---|
| [Repaired English denial](https://yuchi-wang02.github.io/csm-copilot/?probe=callback_denial_en#triage-review) | An explicitly denied callback should not trigger callback troubleshooting |
| [Chinese denial with a separate symptom](https://yuchi-wang02.github.io/csm-copilot/?probe=denied_with_blank_zh#triage-review) | Keep the positive blank-Offerwall symptom while excluding the denied callback mention |
| [Remaining failure](https://yuchi-wang02.github.io/csm-copilot/?probe=not_failing#triage-review) | A repair has a bounded scope: this wording still produces the unwanted callback category |

Selecting a probe updates the address. Reload, Back and Forward restore its ID. Case and recording changes retain an explicitly selected probe in the browser address. The three copy controls share only their own selection. Missing `probe` uses the first published example; blank, repeated or unknown IDs use the same fallback with a visible notice. In-page evidence navigation preserves practice notes, while reloading starts a fresh practice session.

## What a link contains

Copied case links include four allowlisted display settings: `case`, `view`, `lang`, and optional `update=1` or `update=2`. Copied recording links include only `run`; triage links include only `probe`. The account is derived from the integration in the public workflow, so a link cannot combine one customer's identity with another customer's integration. Invalid or duplicated settings fall back to defaults and produce a visible notice. Unrelated query parameters are excluded from all three copied link types.

Copied links always use the project's public website address, including when the demo is run locally. They contain no local filesystem path, practice note, drafted free text, identity token, or private account information. Copying prepares a URL; the application does not send it to another person.

These are links to the current published demo, not immutable snapshots. Future fixture changes may change what a link displays. For a fixed historical record, cite the Git commit and its checked-in evidence files.

## Verification

Eleven routing tests cover every published integration across all review steps, both languages and all three comparison states; every published recording and triage probe; stable selection when a new recording is added; unknown or duplicated settings; independent case/run/probe restoration; public-origin and parameter boundaries; and invalid internal selections. Browser verification separately covers direct links, clipboard contents, history navigation, practice-note retention, the updated comparison, and mobile layout.

Run both browser-logic suites with:

```sh
node --test tests-js/practice.test.cjs tests-js/review-links.test.cjs
```

These checks establish navigation behavior, not the truth of the underlying synthetic evidence.
