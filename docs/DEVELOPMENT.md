# Development notes

## Verified integration issue: structured MCP output

The first engine test run passed, but the real stdio smoke test failed. The client expected `structuredContent`; the server exposed tool return annotations as bare `dict`, and the installed SDK returned text content instead.

The fix was to annotate results as `dict[str, Any]`. A fresh stdio run verified tool discovery, seven structured results, prompt retrieval and invalid-ID error behavior. The test remains in `scripts/mcp_smoke.py` so direct Python tests cannot conceal a protocol integration regression.

**Lesson:** testing a function is not the same as testing the interface a client actually uses.

## Visible baseline failures

The lexical triage method gets 14 of 18 family-separated diagnostic messages correct. It misses indirect no-offer wording and retrieves a symptom even when the customer negates it. Those cases remain in the report. The promise lint also misses two unsupported assertions and flags one negated promise.

**Lesson:** a readable baseline is useful when its limits remain visible. Passing a tiny synthetic suite would not establish reliability in customer communication.

## Contribution and learning status

This implementation was created with substantial AI assistance after Yuchi selected a realistic CSM workflow as the portfolio focus. Synthetic data, tests and documentation were produced during the same development effort. Personal mastery exercises are pending. Later human-authored notes, independent cases and personally implemented changes should be recorded as additional evidence rather than retroactively attributed to this initial build.
