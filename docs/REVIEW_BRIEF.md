# A review packet a person can take away

The static explorer offers two downloadable Markdown briefs. Both are generated from the exact workflow packet used by the page; the second contains Chinese customer drafts while keeping the review structure in English.

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

## Use it in an interview

Open the brief and point to one account. Explain why it was selected, which platform needs evidence, which next action is proposed and which source records support the decision. Then switch to its other platform and explain why the follow-up purpose changes.

For a learning exercise, write your own follow-up for a complete checklist with an old recorded issue. Compare it with the generated draft. Identify which statements are supported by records, which are questions, and which would require new information.

## Limits

These are deterministic templates and exports. No live model quality, customer response, time saving or independent human agreement has been measured. The export preserves the original workflow's limitations, including scoped readiness, synthetic evidence and unconfirmed root causes. It does not make a historical snapshot current merely by exporting it today.
