# A review packet a person can take away

The static explorer offers full-queue and selected-platform Markdown briefs. All are generated from the exact workflow packet used by the page; Chinese variants contain Chinese customer drafts while keeping the review structure in English.

- [English review brief](../evidence/morning-review-en.md)
- [Review brief with Chinese drafts](../evidence/morning-review-zh.md)

Each brief includes the queue and snapshot, separate platform decisions, a proposed CSM next action, customer drafts, technical handoff fields, missing information, field source IDs, and an evidence index. It is a portable synthetic example, not a record of real outreach or model inference.

## Four distinct follow-up purposes

| Condition | Purpose | Next step |
|---|---|---|
| Any scoped check is unknown or not met | Evidence request | Ask for the specific missing/retest evidence and reassess when it arrives |
| Checklist complete, but an issue remains recorded | Issue-status review | Confirm the issue's current status; do not infer resolution |
| Checklist complete, no issue recorded, account live | Post-launch check-in | Ask about the live experience, new issues and configuration changes |
| Checklist complete, no issue recorded, account not live | Launch-plan review | Confirm changes and review the proposed plan; do not promise approval |

This is an explicit project operating policy. Issue records do not have a resolution lifecycle in this prototype, so their presence prompts a status question rather than a claim that the issue is still open or already resolved. Account stage is supplied by the synthetic record; it is not inferred from a target date.

Both languages use the same intent decision. A complete checklist no longer asks for unspecified missing updates. A complete technical handoff moves to human review rather than asking for fields already supplied.

When a handoff has `needs_scope`, the export asks the CSM to clarify the request, desired outcome and relevant account or product before collecting technical details. It does not frame generic field gaps as the next intake request or present populated fields as sufficient. Recorded fields, the original issue text, source references and neutral clarification questions remain inspectable. For example, an invoicing request does not become a technical-support case merely because an SDK version is available or logs are missing. This matches the browser's scope-first review; it does not establish a billing procedure or verified issue classification.

The v0.27.2 repair was reproduced with the same synthetic request, “Please explain invoicing.”, under two intake conditions. The tool returned `needs_scope` in both; only the exported presentation changed:

| Recorded intake condition | Previous exported message | Current next step |
|---|---|---|
| Reproduction steps and logs absent | Missing information: `reproduction_steps, redacted_logs` | Clarify request scope before requesting technical details |
| All five generic fields populated with unreviewed placeholders | Missing information: None in the scoped required fields; human review is still required. | Clarify request scope; populated fields do not establish it |

These are regression examples, not customer observations. [Tests covering both draft languages, retained sources and unchanged input](../tests/test_collection_requests.py).

## Generate an export

```sh
csm-demo --format markdown --lang en --output morning-review.md
csm-demo --format markdown --lang zh --output morning-review-zh.md
```

Without `--output`, the CLI writes UTF-8 to stdout. `--format json` remains the default and preserves the complete machine-readable workflow with both languages. Generate the website's two download files and corresponding checked-in evidence with:

```sh
python scripts/build_demo.py
```

CI regenerates the files and compares them with the committed versions. The exporter does not change source records or contact timestamps. Customer strings are escaped as text in Markdown; they cannot become raw HTML or executable Markdown links in the export.

## Export one platform

The case panel offers two download links for the selected app/platform. They update when the account or platform changes, including when returning through browser history. Each file includes the selected platform's readiness and next action, customer draft, every recorded handoff on that platform, and an evidence index. Account-level contact evidence is retained to explain selection; other accounts and platforms are excluded. A platform without a recorded issue says so without claiming that no issue exists or that an old issue was resolved.

- [Harbor Android handoff and evidence](../demo/case-briefs/harbor_android-en.md)
- [Lantern iOS review with Chinese customer draft](../demo/case-briefs/lantern_ios-zh.md)

```sh
csm-demo --format markdown --integration harbor_android --lang en --output harbor-handoff.md
csm-demo --format markdown --integration lantern_ios --lang zh --output ios-review-zh.md
```

Only integrations present in the morning queue can be exported. Unknown, ambiguous or unqueued IDs fail before writing a file. `--integration` requires `--format markdown`; the JSON workflow remains complete. The optional argument on the Python renderer is `render_review_brief(workflow, lang="en", integration_id="harbor_android")`.

**Snapshot boundary:** the case export always uses the original evidence. The separate synthetic-update toggle does not change it. Each file labels this boundary and its snapshot date. Exporting does not refresh evidence, send a message or reset contact history.

The builder generates eight files: four queued integrations in two languages. CI checks their contents against the renderer and repeats all eight CLI exports from an isolated installed wheel. Scope tests check that iOS cannot inherit Android evidence or handoffs, that all issues on the selected platform survive export, and that rendering leaves the input unchanged.

Platform briefs use UTF-8 with LF line endings. Artifact tests and installed CLI checks compare bytes, so Windows and Linux exports match the files served by GitHub Pages.

## Use it in an interview

Open the brief and point to one account. Explain why it was selected, which platform needs evidence, which next action is proposed and which source records support the decision. Then switch to its other platform and explain why the follow-up purpose changes.

For a focused leave-behind, download the selected platform instead of the entire queue. Explain why its account contact record is included but the other platform's readiness evidence is absent.

For a learning exercise, write your own follow-up for a complete checklist with an old recorded issue. Compare it with the generated draft. Identify which statements are supported by records, which are questions, and which would require new information.

## Limits

These are deterministic templates and exports. No live model quality, customer response, time saving or independent human agreement has been measured. The export preserves the original workflow's limitations, including scoped readiness, synthetic evidence and unconfirmed root causes. It does not make a historical snapshot current merely by exporting it today.
