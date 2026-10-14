# Share a specific review

The **Copy this review link** button produces a public URL that opens the selected synthetic integration, review step and client language. The comparison toggle is also preserved. The **View share link** control exposes a selectable URL if clipboard permission is unavailable.

Use these examples to start an interview at a concrete decision:

| Example | What to demonstrate |
|---|---|
| [Android evidence](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en#workspace) | Unknown settings and a recorded failed device check lead to different requests |
| [Chinese iOS follow-up](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_ios&view=followup&lang=zh#workspace) | A complete scoped checklist leads to launch-plan review, without a promise of approval |
| [Harbor's technical handoff](https://yuchi-wang02.github.io/csm-copilot/?case=harbor_android&view=handoff&lang=en#workspace) | HTTP 405 is a clue rather than a confirmed root cause; missing logs and reproduction steps remain visible |
| [Android after two confirmations](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en&update=1#customer-update) | The separate comparison changes two settings while retaining a failed device check |

## Navigation behavior

Changing the account, platform, review step, language or comparison toggle updates the browser URL. Back and Forward restore the previous selection. Direct links work on the static GitHub Pages site without a server route or login.

The iOS practice evidence link opens the iOS follow-up; the Android practice link opens the updated comparison. These links navigate within the loaded page, preserving practice notes. Opening a new tab or reloading still starts a fresh practice session.

The comparison toggle applies only to the separate counterfactual section. The account workspace always shows the original snapshot, with its original drafts and handoffs. This prevents the comparison from silently altering the evidence being reviewed.

## What a link contains

Only four allowlisted display settings are included: `case`, `view`, `lang`, and optional `update=1`. The account is derived from the integration in the public workflow, so a link cannot combine one customer's identity with another customer's integration. Invalid or duplicated settings fall back to defaults and produce a visible notice. Unrelated query parameters are excluded from copied review links.

Copied links always use the project's public website address, including when the demo is run locally. They contain no local filesystem path, practice note, drafted free text, identity token, or private account information. Copying prepares a URL; the application does not send it to another person.

These are links to the current published demo, not immutable snapshots. Future fixture changes may change what a link displays. For a fixed historical record, cite the Git commit and its checked-in evidence files.

## Verification

Five routing tests cover every published integration across all review steps, both languages and both comparison states; unknown cases; invalid and duplicated settings; public-origin and parameter boundaries; and invalid internal selections. Browser verification separately covers direct links, clipboard contents, Back navigation, practice-note retention, the updated comparison, and mobile layout.

Run both browser-logic suites with:

```sh
node --test tests-js/practice.test.cjs tests-js/review-links.test.cjs
```

These checks establish navigation behavior, not the truth of the underlying synthetic evidence.
