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

## v0.10.1: keep a substring collision from becoming a technical handoff

The no-offers pattern matched `blank` inside `blanket`, so an invoice request could retrieve Offerwall checks. Similar collisions appeared in `casino offers` and `no adservers`. Before editing the engine, twelve diagnostic inputs were run against commit `a3ddd29` and their full results were saved in [the pre-change record](../evidence/triage-boundary-before.json).

The repair adds Latin-letter boundaries around the English no-offers phrases. Common blank inflections and plural offerwalls remain supported, and Chinese characters can directly adjoin English signals. Chinese patterns and reward/callback retrieval are unchanged. Four collision probes now return unknown scope; six positive probes retain their categories. Two known negation/paraphrase failures remain incorrect. The original 30-message diagnostic inputs and 14/18 result are unchanged.

Six regression checks failed before the repair and passed afterward, including ticket variants with complete/incomplete generic fields. The blanket-invoice example now stays with the CSM for clarification instead of receiving a proposed technical owner. This does not establish a billing diagnosis or a Finance routing rule. Real MCP calls exercise both the invoice rejection and a mixed Chinese/English positive message.

**Lesson:** inspect why a term matched before adding more categories. A small lexical repair can prevent a specific bad handoff without solving semantic triage. Preserve both the corrected examples and the unresolved failures. The [paired report](../evidence/TRIAGE_BOUNDARIES.md) is a development diagnostic, not independent validation.

## v0.11: observe whether the model turns correct routes into useful questions

A third prescribed task asks the model to triage two exact inbound messages without supplied account IDs: the blanket-invoice development example and a blank Android Offerwall. Coverage requires two successful calls on the original messages with no assigned integration. Repeating one message or assigning it to a known account cannot satisfy that coverage check.

One actual local Qwen3-4B attempt made both calls in a batch and then produced a final answer. No extra calls, tool errors, schema constraints or host correction requests occurred. The final response separates clarification from evidence collection and states nothing was sent. It uses tentative wording and invents no account IDs, evidence IDs or confirmed internal owner.

The invoice questions follow the tool's generic app/platform and expected-versus-observed fallback, which fits a technical symptom better than an invoice request. This is an AI-assisted customer-fit judgment, not an independent score. The answer could also explain more explicitly that a lexical candidate is not a diagnosis. The task reuses a development probe; it is not held out and no paired model comparison against the older engine was performed.

The original eight traces remain unchanged. The new task, actual calls, unedited response and review are visible in the replay. The PDF count updates to nine attempts, and the interview/learning guides ask the reader to assess the invoice questions before reading the annotations.

## v0.11.1 — let an unknown request remain nontechnical

The ninth model attempt exposed a tool-design problem: the invoice was correctly classified as unknown, but the fallback still asked about an affected app/platform. Three unknown-intent cases and four handoff variants failed their new scope-question expectations against the prior implementation (7 failed, 8 passed in the focused pre-change check). The engine and handoff view now ask for request, outcome and account/product context. Recognized Offerwall questions and the original diagnostic classifications remain unchanged.

A fresh local Qwen3-4B attempt repeated the same task, initial messages, runtime settings and first action batch. Only the invoice question list differs in the tool results. The final answer now repeats the neutral questions and calls the outputs candidates. It still needs customer-specific editing and does not fully explain the retrieval limitation. The old nine recordings were preserved; the tenth records what the model actually generated, with no host corrections.

The lesson is concrete: an assistant can faithfully copy an inappropriate tool suggestion. Review the questions a tool supplies as carefully as its category and route. This is an AI-assisted development observation, not a claim that Yuchi independently performed or mastered the exercise. [Paired evidence](LOCAL_MODEL.md#v0111-neutral-questions-for-an-unknown-request).

**Lesson:** a model can follow tool output and still ask a poorly matched question. Review tool execution, factual support and customer usefulness separately. Fixing the lexical input boundary did not establish that every downstream question is useful.

## v0.12 — open the evidence you mean to show

The AI-section anchor always selected the latest recording. That made older interview examples drift when new recordings were published, and selecting a run was lost on reload. A catalog-validated `run` parameter now identifies an exact published attempt. The copy button emits a public recording-only URL; the separate case button retains its case-only behavior. Browser history restores both views without clearing practice state. Unknown or repeated recording IDs display a notice rather than silently pretending the requested trace was found.

The interview guide now links directly to the original batch failure and the two inbound-message attempts. The PDF opens the constrained recording discussed on its second page. Tests cover all ten published IDs and preserve an older link when a future catalog entry is appended. These changes improve evidence navigation; they add no model-quality result or claim of personal mastery.

## v0.13 — exclude a denied mention without losing another issue

The lexical baseline treated an explicitly denied no-offers symptom as a positive signal. Twenty development probes were frozen with actual pre-change outputs at commit `0308c77`. Twelve regression checks failed before the repair: ten message cases and two handoff variants. The matcher now excludes only signal occurrences inside supported local denial patterns. Other occurrences and callback signals are evaluated separately, and the result records an exclusion note.

The original 30-message dataset and labels remain unchanged. Because its inspected negation cases informed this rule, the current 16/18 is labelled a replay after adaptation. The earlier 14/18 result and failures are preserved. Qualified negation, quoted search topics and callback denial remain explicit counterexamples. No new model inference or independent human/customer validation is claimed. [Paired outputs, workflow consequences and limits](../evidence/NEGATION_REVIEW.md).

## v0.14 — show when the supporting record was captured

Dates were present in raw records but hard to compare in the case explorer. A descriptive timing view now exposes source type, timestamp, snapshot-relative age and supported checks. The same Python helper supplies workflow timing data and Markdown exports; the browser does not recalculate age from its current clock. Shared sources are deduplicated, and missing or mis-scoped sources remain unavailable.

The synthetic settings update is visibly newer than the retained failed device test. This supports a concrete CSM explanation without adding a vendor expiry threshold, automatic readiness change or newest-record-wins rule. The original case packet, historical MCP responses and ten recorded model attempts remain intact. [Design and verification](EVIDENCE_TIMING.md).

## v0.15 — change the next question when the checks pass

The update comparison now has three states: original evidence, two customer-confirmed settings, and additional passing device/callback test records. The final state uses the existing engine rule to generate an `issue_status_review` follow-up. Completing the scoped checklist does not delete the previously recorded customer issue or assert resolution, launch approval or ad availability.

The synthetic branch explicitly replaces the two check references; this is not an automatic newest-record-wins policy. The original snapshot, failed record, platform exports and practice scenario remain intact. The UI shows callback state alongside the other three changed checks, identifies the new records as tests, and exposes the earlier issue and generated draft. `update=1` retains the earlier settings-only meaning; `update=2` restores the new comparison. Reset and browser history restore the relevant state.

**Interview discussion:** explain why the new evidence changes the checklist and the next customer question, but does not answer whether the customer's earlier experience is now resolved. This is a development example, not a record of a real customer outcome or completed personal learning exercise.

## v0.15.1 — give the audience a short route through the evidence

The hero previously sent visitors to a long GitHub document for the three-minute walkthrough. An on-page route now presents three questions: what the CSM should ask next, whether correct tool calls produced a faithful answer, and how to explain a decision before seeing guidance. Each card points to an existing case or exact recorded attempt. It reuses the in-page navigation that preserves practice notes, with return links beside the relevant sections.

The route makes the project's evidence easier to inspect without adding a new model result or claiming personal mastery. Its suggested timing has not been measured with interviewers. Desktop and mobile inspection verify presentation and navigation only; audience usefulness remains unvalidated.

## v0.15.2 — keep unfinished reasoning in the download

Inspection found that the download was disabled until a decision had been reviewed, and the exporter omitted reasoning from unreviewed decisions. That encouraged revealing guidance merely to save work and lost draft notes in a mixed-session export. The download now becomes available after a choice or nonblank note, and preserves unfinished choices and reasoning under explicit draft labels. It does not reveal guidance or change review state.

The AI exercise's evidence link also pointed to the model section's default (latest) attempt despite using the constrained recording. It now opens that exact recording. Four focused regression checks failed before the repair and pass afterward, covering early download availability, unfinished and mixed-session exports, and the recording target. User text remains escaped; saving does not certify authorship or mastery and does not create a resumable browser-session file.

## v0.16 — make the first terminal run readable

The CLI's default JSON is useful for inspection but too large for a quick first explanation. `--format summary` now provides a compact English view of the original workflow queue, app/platform decisions, unknown and failed checks with record IDs, next actions, and scoped handoff missing fields and owners. It consumes existing workflow results without model inference or state changes. Markdown and JSON remain the detailed exports; unsupported summary/language or summary/platform combinations fail before writing.

The generated plain-text artifact is verified against the installed CLI on both CI operating systems. Behavioral checks cover platform separation, original-snapshot scope, unknown contact history, a missing handoff draft, an empty queue, terminal-control characters, UTF-8 stdout/file agreement and incompatible options. The learning guide introduces a source-tracing exercise using this short output. A stale README paragraph describing the earlier inbound-message attempt as newest was also corrected against the preserved recordings.

## v0.16.1 — keep rounded display values out of queue ordering

Input-boundary inspection reproduced a chronological sorting error. Two planned launches at 09:01 and 09:02 UTC both displayed as `2.0` days away; sorting that rounded value then used account ID to put the later launch first. The engine now sorts exact timezone-aware timestamps and uses account IDs only for actual timestamp ties. Optional live accounts remain at the end.

| Synthetic case | Before repair | After repair |
|---|---|---|
| Future launches one minute apart | Later launch first because both rounded to 2.0 days | Earlier timestamp first |
| Overdue launches one minute apart | Later launch first because both rounded to zero days | Earlier timestamp first |
| Nearby launches expressed with different UTC offsets | Rounded values caused an artificial tie | Actual instants determine order |

[The original three outputs](../evidence/queue-order-before.json) were captured at `e4773be` before the change. Each case changes only two target timestamps in a copy of the bundled fixture; the file records the original fixture hash and expected order. Three focused tests failed before the repair and passed afterward. A fourth check retains account-ID ordering for actual ties and keeps live accounts last. Tests also confirm that returned values, selected accounts and input records are unchanged; only their order differs. The default portfolio queue and recorded model traces are unchanged. These are developer-authored regression cases, not customer outcome evidence.

## v0.16.2 — distinguish a later review clock from refreshed evidence

`list_accounts(as_of=...)` already recalculated dates from a fixed dataset, but the output showed only the requested calculation timestamp. It now also exposes `dataset_as_of`, `time_basis`, `records_refreshed: false` and a time-boundary explanation. Equivalent instants written with different offsets are classified as the dataset snapshot. A later instant is a recalculation; the stored contacts, stages, launch dates and readiness remain unchanged.

An explicit empty date previously fell through to the default timestamp. It now fails like other invalid date strings; omission or null still selects the snapshot. Four focused checks failed before this change, and all five now pass. The real stdio MCP client verifies both a later-date call and empty-date rejection. Historical model traces remain unedited. This clarifies time provenance; it is not a freshness policy or a live data integration.

## v0.17 — make handoff questions readable and portable

The handoff panel previously exposed candidate questions only inside a JSON disclosure, and Markdown exports omitted them. The panel and exports now show the original issue record, candidate-specific questions, related documentation and triage notes beside the known and missing fields. The raw result remains available for inspection. Unknown requests receive a clarification heading rather than a technical diagnosis.

The questions are suggestions from the existing lexical baseline, not a tailored customer message. Harbor's record already supplies a currency mode and time window, so a CSM should reuse those facts and ask only for unresolved details. The page explicitly asks the reviewer to inspect known information first. HTTP 405 remains a hypothesis prompt, not a confirmed cause. No tool output, routing decision, source record or historical model answer changed.

Five focused checks cover readable questions, multiple candidates, unknown requests, original source scope, markup safety and export preservation. The browser only creates clickable HTTPS documentation links; other source values remain escaped text. The interview and learning guides now ask the reviewer to remove redundant questions using the original record before drafting a follow-up. This is a presentation and review-workflow improvement; customer usefulness has not been measured.

## v0.17.1 — identify the original issue source

The data model permits an issue to reference a customer report or a test record, but the evidence panel always labeled it a customer report. Labels and disclosure text now follow the source kind, with an explicit unavailable-type fallback. The handoff disclosure and exported brief also show the record type and timestamp.

The Markdown exporter previously quoted `ticket.customer_report`, a copied string whose legacy name does not establish source type. It now resolves the issue's original record using the issue ID, evidence ID, account and platform. A missing, ambiguous or differently scoped source produces an unavailable-source message instead of quoting the copied field. This is a presentation-layer consistency check; it does not authenticate the underlying record or verify its meaning. Tool schemas and historical model recordings are unchanged.

Seven focused regression checks failed before the change and pass afterward. They cover customer/test labels, missing type, original-versus-copied wording, and missing or differently scoped records. Existing markup tests now insert their probe into the original source record as well as its copied field. The two bundled customer reports remain customer reports; no example was relabeled to manufacture test evidence.

## v0.18 — practice a focused callback handoff

A fourth practice decision now draws from Harbor's original issue record, existing handoff fields, missing-field list and unconfirmed root cause. It asks the reviewer to distinguish redundant questions, a focused evidence request and a premature diagnosis. Guidance explains why the supplied currency mode, SDK, region and time window should be reused, and why a new callback example should be tied to the relevant attempt.

The existing reflection flow preserves initial choice/reasoning and later revision separately. The new source link opens Harbor's exact handoff in-page. Reset now derives its count from the case collection instead of announcing three decisions. The earlier three cases and historical model outputs remain unchanged. Two added tests verify evidence grounding and fourth-case export preservation; existing export-count assertions now follow the case collection.

The teaching text is AI-assisted project guidance. It does not grade prose, certify personal mastery or establish customer usefulness. Browser-test notes explicitly identify themselves as QA material; Yuchi's own exercise has not been completed on their behalf.

## v0.18.1 — preserve evidence as text in reflection exports

Reflection exports already escaped user-authored notes, but evidence labels, values and source IDs were inserted directly into Markdown. A customer report containing HTML or Markdown syntax could therefore change the document's presentation. Three probes reproduced this separately for labels, values and source IDs.

The exporter now shares its literal-text escaping between notes and evidence. Evidence lines normalize CRLF, CR and LF to spaces before insertion, while user notes retain their quoted line breaks. Source IDs keep their original meaning with escaped Markdown punctuation. The actual records, teaching cases, browser evidence and historical model outputs are unchanged. Three regression checks pass after failing before the repair; earlier tests continue to check original reasoning, later reflection and unreviewed exports. This addresses the exercised Markdown/HTML formatting cases, not every behavior of every third-party Markdown renderer.

## v0.19 — exclude explicitly denied callback mentions

The preserved no-offers review included a callback-denial counterexample: an invoice request saying the reward callback was not the problem still produced callback troubleshooting. Sixteen additional before-change outputs are now frozen at `b1a7ca2`, including selected repairs, positive controls and three remaining failures. A shared occurrence-scoping helper applies separate no-offers and callback denial patterns; only matched occurrences inside a supported denial span are excluded.

Seven selected English/Chinese messages change categories. Four handoff variants also keep denial-only requests with the CSM even when all generic fields are supplied. A different positive callback mention survives, as does a separate blank-Offerwall symptom. Eleven checks failed before the repair; all twenty new checks now pass, including checks that preserve the documented limitations. The old twenty-probe input file remains unchanged, with its callback case still marked as a historical known limit and separately recognized as repaired by the current test.

The original thirty-message diagnostic stays at 16/18 after earlier adaptation, and all ten raw model recordings are unchanged. The real MCP transcript includes two new denial calls. This is an inspected lexical correction, not new model evaluation or independent customer validation. [Frozen outputs, current replay and limitations](../evidence/CALLBACK_DENIAL.md).

## v0.20 — expose the triage comparison in the portfolio

The callback-denial comparison was available as a Markdown/JSON report but required leaving the case explorer. A new on-page selector presents all sixteen preserved messages with before/current category sets, project expectations, the current route, uncertainty and exclusion notes. A status distinguishes changed matches, unchanged matches and remaining mismatches. Original outputs and the development report remain linked; a disclosure exposes the current tool result.

The demo builder now regenerates and embeds the same comparison report in one step. The browser renders recorded outputs without running triage or a model. Four checks verify exact report equality, repaired routing, known failures/separate positive symptoms, non-mutation and escaped text. The original diagnostic, expectations and model recordings are unchanged. This improves inspectability; no audience-usability or customer-outcome measurement is claimed.

## v0.20.1 — share an exact triage example

The explorer now gives each published probe a public URL. Selection, reload and browser history use the same catalog allowlist; invalid or duplicated IDs show an explicit fallback notice. Case and recording controls retain a selected probe in the browser address, while each copy button includes only its own public selection. In-page evidence navigation continues to preserve practice notes.

Three added routing tests cover all sixteen probes, stability when the catalog grows, malformed IDs, independent case/run/probe restoration and exclusion of unrelated content. The sharing guide now links directly to a repaired English denial, a Chinese message with a separate positive symptom and a remaining failure. This changes review navigation, not the triage algorithm, expectations or historical model recordings.

### Deployment recovery — identify the artifact by run and attempt

The first v0.20.1 Pages deployment reached `updating_pages` and timed out after ten minutes. Re-running that workflow produced a second artifact named `github-pages`; the deploy action rejected the ambiguous selection. The application CI passed independently. The [first failure](https://github.com/Yuchi-Wang02/csm-copilot/actions/runs/38594474337/attempts/1) and [retry failure](https://github.com/Yuchi-Wang02/csm-copilot/actions/runs/38594474337/attempts/2) remain in the workflow history.

Upload and deployment now use the same artifact name containing the workflow run ID and attempt number. A retry therefore has its own artifact without deleting the earlier upload. This addresses the observed artifact-selection failure; it does not prevent GitHub Pages service delays or establish that a deployment succeeded. The deploy action and the public page must still be checked. The setting uses the official [upload `name` input](https://github.com/actions/upload-pages-artifact/blob/v3/action.yml) and [deployment `artifact_name` input](https://github.com/actions/deploy-pages/blob/v4/action.yml).

### Reproducible interview bundles

The initial downloadable demo was packaged outside the repository. Its first byte comparison caught Windows line-ending conversion; conversion was disabled before the verified package was published. A checked-in builder now reads the selected committed tree directly and creates a deterministic archive with fixed metadata. Dirty worktree changes and untracked notes stay out, and missing static references stop packaging.

Six focused checks exercise those boundaries using temporary Git repositories. CI now builds and uploads the same selected commit on Windows and Ubuntu so the inner ZIP hashes can be compared. This introduces a new bundle format rather than rewriting the first release asset. [Build instructions and verification limits](INTERVIEW_BUNDLE.md).

## v0.21: practice questioning a tool recommendation

The fifth practice decision presents the preserved `not_failing` customer message alongside the current callback candidate and collection questions. It draws evidence directly from the generated diagnostic report; expected categories are absent from the pre-guidance evidence. The recommended response acknowledges invoicing and clarifies context without claiming callbacks were verified healthy or inventing a Finance deadline.

The source link opens that exact failure in the triage review. Initial reasoning, later reflection and unfinished work remain separately labeled in exports. Two additional JavaScript checks cover source grounding and fifth-case state/export behavior. The classifier, diagnostic scores and historical model recordings are unchanged; this is an opportunity to explain review judgment, not evidence of improved model reliability or completed personal learning.

## v0.21.1: share a decision before guidance

Practice now has a stable public ID per decision, a copy button and a selectable URL fallback. URLs select the exercise only; answers, revealed state and notes remain in page memory. The existing review router preserves an explicit practice selection when opening evidence or changing case/recording/triage controls. Back and Forward select the appropriate decision without discarding the session; reload starts unanswered, and reset clears all work and selects the first decision.

Three additional routing checks cover all five IDs, catalog reordering, invalid/duplicate input and independent restoration with private-note exclusion. Browser verification covers the integrated event flow. During local QA, the previous versioned scripts were still cached; the release asset version was advanced before checking the new behavior. No classifier, model recording or customer evidence changed.

## v0.22: distinguish text, action authority and answer truth

A new six-probe report makes the existing trust boundaries inspectable. Instruction-bearing source text remains visible while structured readiness, queue and follow-up remain unchanged. The single/batch parser rejects unavailable send/update tool names; it still accepts an unsupported final statement, and the demo allows reads of other synthetic accounts. The report exposes those limits rather than calculating a safety score.

The browser replays the report generated by `evaluation/trust_boundary.py`; six tests check exact source retention, scoped state preservation, parser rejection, accepted limitations and reproducibility. There is no model inference, external dispatch or change to historical recordings. This addition provides a concrete interview discussion about controls without claiming that a prompt alone prevents injection or that read-only tools establish truthful answers.

## v0.23: a bounded repair to the preserved callback failure

Twelve callback-health messages were captured against commit `063583e` before the change. Five message cases and two handoff cases failed the new expectations; seven controls/known-limit checks passed. Adding a present-tense denial span made all fourteen checks pass while retaining qualified, question, past-tense and separate-positive behavior. The quoted-topic mismatch remains visible.

The old sixteen-case fixture is unchanged. Its generated replay retains the original kind and complete raw result while labeling `not_failing` as a current repair. The fifth practice decision deliberately uses that historical result, and its evidence link shows both before/current outputs. The thirty-message diagnostic remains 16/18; no independent improvement estimate or new model inference is claimed.

## v0.24: make the immediate intake request specific

Harbor's generic callback questions asked for a time window even though the structured handoff already contained one. The handoff now adds a focused request for missing fields from the project's five-field intake policy. Harbor requests reproduction steps and redacted logs; its recorded SDK version, region and time window remain traceable. The browser presents this request before the original report and keeps broader candidate questions in an expandable review section. The Markdown export carries the same focused request alongside the original suggestions.

Unknown issue scope produces no technical collection request, regardless of generic field completeness. Complete fields still require human review. The policy does not extract details from free text, validate the quality of populated values, or establish that the five fields are sufficient for every issue. It is project intake wording, not an official support requirement or a measured customer-experience improvement.

Seven new Python checks initially failed because the request field/export did not exist. After implementation, they cover Harbor's omissions, complete/incomplete unknown scope, unreviewed populated fields, whitespace versus free-text details, per-issue isolation and Markdown presentation. Two JavaScript checks cover presentation order, escaping and visible scope clarification. The real stdio MCP smoke check verifies the additional output. Historical model recordings remain unchanged.

## v0.25: resume personal practice without implying verified history

Readable Markdown notes could be saved, but could not restore an unfinished practice session. A separate local JSON checkpoint now preserves selected decisions, draft choices, original responses and later reflections. Choosing a file only validates and previews it; an explicit replacement action applies it. Invalid files, stale asynchronous reads and cancelled previews cannot replace the current work.

The loader accepts only the current decision catalog and validates state consistency and note lengths. A content signature detects changed exercises while allowing stable-ID reordering. It imports no evidence or guidance. Restored work is labeled in the UI and Markdown export as user-editable file content, not verified history. Six tests exercise round trips and rejection boundaries; browser checks cover the actual file download, preview and resume interactions. The project still does not evaluate written reasoning or claim personal learning outcomes.

## v0.26: make model, host and tool activity distinguishable

The AI replay previously placed its full conversation in a single JSON block. A new turn view makes each model proposal, MCP result, host rejection and correction request individually inspectable. The constrained attempt visibly progresses through two rejected structured responses and host-supplied feedback before matching fields. Its explanation remains unverified. Early parser failures show that no calls executed in that turn; a later tool error remains separate from other calls that received results.

The renderer reads the ten existing traces, escapes all source content and retains the initial instructions and raw steps. Seven JavaScript checks cover recording preservation and the different failure/control paths. This improves how the evidence can be explained; it adds no inference, new accuracy result, independent review or measured audience-comprehension outcome.
