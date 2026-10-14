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

## v0.6: formatting, field agreement and prose are separate checks

A structured contract alone did not solve the response problem: the local model generated malformed nested JSON and repeated it after both correction requests. An optional LM Format Enforcer integration then produced parseable JSON, but the field reviewer rejected duplicated platform entries and an issue-only source incorrectly placed in readiness evidence. After two recorded corrections, the fields matched.

The original outputs, feedback and failures are retained. A system-rendered summary uses the observed tool results only after the field match; model prose stays separate and unverified. Its final explanation still omits inline citations and an explicit nothing-sent sentence, despite supplying those facts in structured fields. Tests explicitly show that matching fields cannot certify arbitrary prose.

**Lesson:** a model can satisfy a format constraint while selecting wrong evidence or repeating a platform. Schema constraints, field checks and explanation review answer different questions. A successful assisted correction is not an independent accuracy result.

## v0.7: make the learning process visible

The portfolio previously provided written exercises but no place to preserve a first interpretation and subsequent reflection. Three browser decisions now reuse the actual counterfactual, iOS workflow and recorded model-review evidence. Revealing guidance freezes the original response within the session; a separate field captures later reflection. The download labels these stages and any unreviewed cases.

Five Node tests check the source conditions, state transitions, report boundaries and escaping. Browser inspection exercised both matching and differing options, return navigation, reset, keyboard focus, mobile layout and a downloaded reflection. The download event observer timed out, but the actual browser-created file was found and its contents inspected; it retained the original test note and separate reflection. No test notes are published as personal learning evidence.

**Lesson:** an educational interface should preserve how reasoning changes while keeping practice progress separate from validated competence.

## v0.8: let reviewers open the intended evidence

Practice links previously pointed only to the generic workspace anchor. The iOS exercise could therefore open the currently selected Android case, and a manually shared website URL did not preserve the intended review. A small routing layer now restores the public integration, review step, language and comparison toggle. Copying a link always uses the public site origin and excludes practice notes and unrelated parameters.

The in-page practice links use the same route reader without reloading, preserving notes. Browser Back and Forward restore case state. Invalid or duplicate parameters fall back with a visible notice. Five tests cover the routing boundaries and all published display combinations, alongside direct browser checks.

Testing a direct iOS handoff link exposed another wording problem: the empty-issue panel asked for missing evidence despite a completed checklist. It now uses the current follow-up's next action and says that no issue is recorded. The README also replaces the growing release-by-release introduction with links organized around what a reviewer wants to inspect.

**Lesson:** evidence can be correct yet hard to review when navigation loses context. A useful portfolio needs reliable entry points and wording that still fits less-common states.

## Portable project brief

A two-page PDF now provides a short introduction for someone who has not explored the repository. It combines the customer problem, a platform comparison, the recorded AI failure and response, contribution boundaries, and clickable evidence links. Its figures are read from the current evidence bundle, with assertions around the case conditions used in the prose.

The first layout overflowed onto a third page; spacing was revised and both rendered pages were inspected. Repeated builds then exposed a metadata issue: setting invariant mode only on a partial canvas factory was overridden by the document template's default. Setting invariant mode on the document itself fixed the byte differences. CI now rebuilds and compares the PDF on both supported operating systems.

**Lesson:** a useful interview artifact needs readable presentation and traceable claims. Reproducibility must be checked on the actual exported file, not inferred from a generation flag.

## v0.8.1: keep caller edits out of the evidence snapshot

An audit found that readiness results exposed the source fact's mutable evidence-ID list. Clearing that list in Python also cleared the engine's source references, leaving a known fact without supporting evidence. The Product digest inherited the same reference. A supplied `Dataset` was also retained directly, so later caller edits could change the engine, and a previously validated but subsequently modified dataset bypassed validation at construction.

Four regression checks failed before the repair. Construction now validates a fresh model dump, which both checks the current contents and creates a separate model tree. Readiness results copy their evidence IDs. All 113 Python tests pass, including checks that a second tool call returns the original result after a caller edits the first result. Existing generated evidence and the portable PDF remain unchanged.

This was an in-process Python ownership bug. MCP's JSON transport already separates a client's result objects from the server's Python objects. The fix does not make engine attributes immutable or establish a security sandbox.

**Lesson:** read-only behavior includes what happens after a function returns. Returning a nested mutable reference can undermine validation even when the function itself performs no assignment to source data.

## Verify what a reviewer installs

The existing CI built a wheel after testing an editable checkout, but did not execute the installed wheel. That left the packaged-resource and console-entry-point claims indirectly checked. A new verifier installs the wheel into a fresh temporary environment, verifies the imported module's location, and runs from outside the repository. It compares the installed CLI's JSON and bilingual Markdown exports and the real MCP console command's transcript with the published artifacts.

The complete wheel passed locally. A disposable wheel with `accounts.json` removed installed successfully but failed when loading the workflow; the new verifier rejected it. The incomplete wheel and its raw local log are not distributed. CI now performs the positive installation check on Windows and Ubuntu. This adds verification without changing the customer workflow or the recorded model results.

**Lesson:** a successful build does not prove that an installed artifact works. Check the path a reviewer actually uses, including packaged data, console commands, and a working directory that cannot supply missing source files.

## v0.8.2: clarify issue scope before choosing a technical owner

The triage baseline returned `clarify_scope` for unrecognized requests, but ticket drafting always proposed Technical Support. Filling all generic fields also produced `ready_for_human_review`, despite the unresolved scope. Four regression checks reproduced the contradiction with English and Chinese summaries, each with complete and incomplete fields.

Ticket drafting now preserves `needs_scope` and proposes CSM clarification first. The UI uses the same state instead of deriving readiness solely from the missing-field count. The structured result retains field missingness for inspection. All 117 Python tests pass, and both scope cases were inspected in a local browser preview. The original fixture outputs and historical model recordings remain unchanged.

**Lesson:** field completeness is not problem understanding. An unrecognized issue may be technical, but the lexical baseline has not established that; the next action should collect enough context for a person to decide.

## v0.8.3: make every scoped issue reviewable

The backend and Markdown export supported multiple recorded issues, but the browser used the first matching issue in both Evidence and Handoff. A local fixture with two Android issues and a separate iOS issue reproduced the omission: only the first Android handoff appeared.

The browser now renders every issue for the selected integration, pairing each summary with its own source and draft. Missing sources or drafts get explicit unavailable messages instead of implying that no issue exists. Five JavaScript checks cover multiple records, platform scope, missing records, escaped customer content and scope-first handoff wording. The complete JavaScript suite contains 15 checks.

The local browser preview displayed both Android reports and drafts, while switching to iOS showed only its own report. The inspected 360-pixel viewport had equal document and scroll widths of 345 CSS pixels, and no browser errors were recorded. [Local regression screenshot](assets/demo-multiple-issues-probe.png). The additional records are clearly labeled local test cases; the public five-account fixture and historical model recordings remain unchanged.

**Lesson:** correct backend output does not guarantee a complete customer review. When the data allows multiple records, inspect whether the interface preserves them rather than silently selecting one.

## v0.9: inspect a second model task

The local host and coverage checker originally hardcoded the four-action platform-follow-up task. They now identify the task explicitly and check its own required actions, while old recordings without a task ID retain their original interpretation. Unknown task IDs are rejected, and the platform-specific structured response contract cannot be used for the handoff task.

One new Qwen3-4B attempt retrieved Harbor's account context and drafted its callback handoff. It also made two extra calls, including triage on an issue identifier rather than customer prose. The explanation cited the issue and preserved several facts, but blurred a failed check with an unconfirmed cause and omitted the owner and specific hypothesis. The trace is retained without correction or rewriting. The replay now exposes each attempt's task and shows account/issue arguments as well as integration IDs.

**Lesson:** successful tool execution can hide an input-meaning error. Coverage, argument suitability, recorded check status, causal uncertainty and final-answer completeness need separate review. A second development task is more evidence to inspect, not an independent benchmark.

## v0.9.1: turn an observed input error into an explicit tool response

Three rejection tests reproduced the issue-ID-as-prose problem; three acceptance cases retained English, Chinese and prose containing an ID. Triage now rejects a bare known issue ID and explains which tool to use. The MCP description states that distinction, and the real stdio check exercises the rejection. The check intentionally does not guess whether every unfamiliar string is an identifier.

A fresh local run repeated the same four-call batch. The extra triage call was rejected while the required context and ticket calls succeeded. The answer distinguished the failed check from causal uncertainty and included a nothing-sent statement, but still omitted evidence IDs, owner and the specific hypothesis. The historical trace remains unchanged; a regression check explicitly preserves its formerly accepted result while expecting rejection from the new engine. New traces record the project version.

**Lesson:** an observed failure can justify a narrow, explainable input check. That check's success does not certify the rest of the model response, and historical evidence must not be rewritten to match newer behavior.

## v0.9.2: compare the evidence without implying a clean win

Switching between two long recordings made the changes hard to assess. The replay now provides a paired comparison. Task text, model revision, sampling settings and the initial action batch are compared directly from the raw traces; the changed system message is also visible. Required-action coverage, all attempted calls and tool errors are separate rows. Explanation judgments remain explicitly AI-assisted annotations.

The comparison exposes a tradeoff: the newer answer preserves the failed-check/cause distinction and says nothing was sent, but loses the earlier source citation. Both answers omit the proposed owner and specific hypothesis. Buttons open either full recording and move keyboard focus to it. Three Python checks cover the recorded counts, changed controls and missing-record handling; the full suite has 132 checks. No new inference was run for this presentation change.

**Lesson:** a useful portfolio comparison should let a reviewer challenge an improvement claim. Show unchanged conditions, changed conditions, gains, losses and remaining gaps rather than reducing the two answers to a winner label.

## v0.10: take away one platform without borrowing another's evidence

The page could share a selected platform but its download contained the full morning queue. A reviewer discussing one handoff had to locate it again inside a larger brief. The case panel now offers English and Chinese-draft exports of the selected platform. The CLI accepts the same scope through `--integration` in Markdown mode.

The renderer selects the platform, all its recorded issues and matching handoffs, and its evidence. It retains that account's contact records to explain queue selection. It excludes other platforms, other accounts and the separate counterfactual branch. A missing issue is described as absent from the snapshot, not resolved. Unknown, unqueued and duplicate platform IDs are rejected before writing. The original workflow is not mutated.

The tests exercise all four platforms in both languages, cross-platform evidence exclusion, multiple handoffs, no-issue wording, invalid scopes and preservation of an existing output file on CLI errors. The package verifier also runs all eight scoped exports from the installed wheel outside the checkout and compares them with the website's downloads.

**Lesson:** a portable handoff needs an explicit scope as well as complete fields. Removing irrelevant records must not remove the evidence that explains the decision, and exporting an old snapshot must not make it appear current.

The public-download check then exposed a byte-level difference: Windows generated 93 CRLF line endings in the Harbor brief, while GitHub served LF. The text matched after normalization, but the SHA-256 did not. Platform-file generation now explicitly uses UTF-8/LF, and both the artifact tests and isolated CLI check compare bytes. The strengthened test failed on the previous generated files and passed after regeneration. The public download then matched the local source without normalization.
