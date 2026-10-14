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

## v0.2: source ownership and handoff identity

A follow-up code audit found that existence checks did not enforce evidence ownership. It also found an unrestricted ticket-details merge that could replace app/platform identity. Nine regression checks were added first and failed against v0.1: cross-platform evidence, wrong-check evidence, another customer's contact, another integration's issue source, three untracked/identity detail fields, a whitespace-only SDK version, and an unknown check name.

The fix adds explicit evidence scope and structured claims, a permitted ticket-details schema, whitespace normalization and per-field source pointers. Further tests cover reversed claims, retained uncertainty, multiple claims in one correctly scoped report, orphan-source ownership, technical claims in contact records, duplicate references and normalized real values. The full suite now contains 44 passing checks, including the eight-case public replay.

The source-provenance improvement does not change the lexical triage score. The existing 14/18 diagnostic result remains visible. New integrity checks are reported separately because they measure a different property.

**Lesson:** a clean fixture can conceal a broken invariant. Test whether deliberately mis-scoped input is rejected, rather than using a passing example to claim that scope is enforced.

## v0.3: move the work to the appropriate next step

A review of completed cases found that the original follow-up still asked for unspecified updates when no checklist evidence was missing. A complete handoff likewise said to request missing evidence. The communication layer now selects an explicit intent: evidence collection, recorded-issue status, launch-plan review or live-account check-in. English and Chinese wording follow the same policy.

The readable export uses the exact workflow packet behind the browser, retaining source IDs, missing fields and the evidence index. Export tests cover both languages, CLI equivalence, repeated read-only rendering and escaping customer markup. A separate test reproduced an ASCII-console encoding failure; stdout now explicitly emits UTF-8 bytes. The v0.3 suite contained 59 checks, and the real MCP client also exercises complete-checklist and live-account follow-ups.

**Lesson:** a correctly populated template can still ask for the wrong next action. Test complete and historical cases as well as blocked onboarding cases.

## v0.4: turn recurring gaps into questions for Product

The morning queue excludes recently contacted accounts, so it would be the wrong population for portfolio feedback. The new digest includes all non-live accounts by default and uses evaluated checklist applicability. It counts distinct accounts separately from integrations; duplicate evidence does not inflate either count.

Ten targeted tests cover a two-platform customer, duplicate supporting reports, unknown versus failed states, managed-currency callback applicability, empty cohorts, record scope, input order, read-only behavior and escaped exports. The full suite now contains 69 tests. The first export assertion incorrectly expected an unescaped underscore in Markdown; it was corrected to match the escaped text while retaining the source-presence check.

Product questions are deliberately labeled as proposals. No extra customer records were authored to create a more impressive pattern, and no customer-confusion or causal claim is inferred from missing evidence. This is a snapshot for discussion, not an automated weekly trend report.

## v0.5: separate model tool choice from answer fidelity

The first actual local model attempts failed the strict single-action JSON contract: Qwen3-0.6B returned a fenced action with an invented date; Qwen3-4B returned four concatenated objects. Both were rejected before tool execution and preserved as raw traces.

A new explicit bounded-array contract accepted a freshly generated four-call batch from Qwen3-4B. The calls succeeded, but the final explanation overstated iOS checklist completion as full compliance, omitted citations and blurred Android's failed check into missing evidence. The narrow promise lint returned zero flags. An AI-assisted source comparison documents these limitations without claiming independent human validation.

The optional offline worker uses an existing local GPU environment, while the host uses the project environment and real MCP stdio. The full 90-test suite includes parser-boundary cases and recording-integrity checks. CI packages the recordings without running inference. This iteration changes the evidence available about the AI workflow; it does not establish model reliability.
