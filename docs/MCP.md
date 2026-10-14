# MCP setup and honest demo modes

The package pins the official Python MCP SDK to `1.30.0`. It uses the SDK's `FastMCP` stdio server and `ClientSession` client. The eight tools return typed dictionary payloads and read-only/idempotent annotations. These annotations describe behavior; they are not a security enforcement mechanism.

## Configure a host

Install the package into a virtual environment. Configure your host to launch that environment's absolute Python executable with `-m csm_copilot.server`. The host starts the process; do not run a second server manually on the same stream. Stdout belongs to the MCP protocol; diagnostics go to stderr.

For Claude Code, after installing its official CLI and signing in yourself:

```sh
claude mcp add --transport stdio csm-copilot -- /absolute/path/to/.venv/bin/python -m csm_copilot.server
```

On Windows, substitute `C:\path\to\.venv\Scripts\python.exe`. Other hosts accept equivalent stdio configuration. Use the host's current official instructions if its format changes.

Sources: [official Python SDK](https://github.com/modelcontextprotocol/python-sdk), [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture), [Claude Code MCP documentation](https://code.claude.com/docs/en/mcp). Reviewed 2026-10-14.

## Suggested live prompt

> At the bundled snapshot, which accounts are more than three days past their last actual contact? Inspect their integrations separately. Draft English follow-ups, a Chinese version for Lantern Games, and technical handoffs for recorded issues. Cite evidence IDs and public source URLs. Preserve unknowns. Do not send anything or claim launch approval.

The exposed `morning_review` prompt contains a more detailed version. A good host run should retrieve the queue, inspect contexts, check integrations and prepare drafts. Tool call order can vary. A correct result matters more than an exact sequence.

## What to inspect in the host output

- Are `acc_014`, `acc_018` and `acc_006` selected at the default snapshot?
- Does Android remain blocked even though iOS passes its scoped checklist?
- Does the host preserve “unknown” currency approval rather than claiming it was rejected?
- Does it treat HTTP 405 as a diagnostic clue, not proof of one cause?
- Does it retain missing ticket fields without inventing SDK versions or logs?
- Does it avoid guaranteed approval, launch, fill and resolution time?
- Does it say drafts were prepared, with no claim that messages were sent?
- Does every factual assertion have an appropriate source?

## Three different forms of evidence

| Mode | What it demonstrates | What it does not demonstrate |
|---|---|---|
| Static interactive replay | Reviewable engine outputs and workflow design | Live model reasoning |
| Scripted stdio client | SDK/protocol integration and tool results | Autonomous tool choice |
| Model-enabled host run | Actual model tool choice and response behavior for that run | General reliability or business impact |

The first two were checked into v0.1. Version 0.5 adds [three local model attempts](LOCAL_MODEL.md) with model revisions, prompts, generated actions, tool results and review notes. Two stopped before tool execution; one completed the requested calls but its final explanation needs revision. No paid inference or independent model benchmark result is included.

## Product feedback workflow

Use the `product_feedback_review` prompt, or call `friction_digest` with `include_live: false` for the default onboarding cohort. Counts describe the fixed dataset snapshot. Ask the host to inspect source records, separate unknown checks from failures, and keep proposed Product questions conditional. No logging or external submission is performed.
