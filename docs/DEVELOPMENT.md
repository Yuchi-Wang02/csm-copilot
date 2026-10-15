# Development notes

## Complete the morning run, then inspect the explanation

One new Qwen3-4B run used source `d5c9f289203da935a3250cd9a125475b4c070f8b`, constrained morning actions and an explicit 600-second response budget. Recorded model/runtime controls, task, initial messages, seven tool actions and results match the earlier constrained attempt. All seven calls completed, and an eighth turn returned an 80-word explanation after 272.986 seconds of final generation. The process exited 0. No correction or retry was used. The raw file is preserved with SHA-256 `aead6eaa015718e276ded9ff568281d5e418b8aadbb01fb10cfd749b6c1fc3e6`; all fourteen earlier raw recordings remain unchanged.

The answer correctly names the missing SDK version, time window and redacted logs. It also groups unknown currency approval and a recorded failed device check as "missing" verification, omits available contact/iOS citations, and describes platform states without explaining their distinct next actions. The replay pairs both the problematic wording and the correct intake list with exact historical fields. This is a completed assisted execution with visible reasoning gaps, not a fully faithful answer or a general model-quality result.

New checks reconstruct all eight request histories and fingerprints, validate policy/schema state and scoped tool results, and reject ambiguous comparison sources. All 432 Python tests, 107 JavaScript tests and Ruff checks passed. Local Edge checks confirmed fifteen attempts, two claim comparisons, eight turns and the final request's recorded 600-second budget. The comparison stacks at a 390-pixel viewport without horizontal page overflow. The refreshed two-page brief retains seven links; both rendered pages were inspected. These checks do not establish independent semantic validation or personal mastery.

The [experiment notes](LOCAL_MODEL.md#longer-response-budget-a-returned-answer-with-reasoning-gaps), interview branch and prediction exercise preserve the observed success and limitations together. This source and recording postdate the fixed v0.29.8 package. The next useful improvement is preserving evidence-state distinctions and actionable platform reasoning in the final answer.

## Preserve the request when a worker fails to answer

The previous model run completed seven tool calls but lost its final in-flight input when the worker timed out. The host now persists the complete request and its byte fingerprint before dispatch, saves the pipe-write state before waiting, and records specific timeout or response failures. Atomic snapshot replacement retains the prior readable file if replacement fails. The response budget remains 180 seconds by default and can be explicitly set from 1 to 600 seconds; the trace records the choice. These changes do not recover the older missing input or establish that a longer wait will produce a faithful answer.

Thirteen added Python checks cover persisted request order, detached message snapshots, first-turn and eighth-turn timeouts, EOF, malformed JSON, invalid UTF-8, dispatch failure, cancellation, atomic replacement failure and CLI budgets. They use scripted workers through the real MCP server, not model inference. A replay-renderer check distinguishes saved requests from returned model proposals and keeps failure text inert. All 422 Python tests, 106 JavaScript tests and Ruff checks passed.

A local Edge check opened an eighth-turn timeout produced by the scripted integration path. It showed the pending request, budget, direct failure cause, complete policy state, final schema and explicit absence of a model answer. This temporary QA output is not published as a model recording. The fourteen historical raw traces remain unchanged; the fixed v0.29.8 ZIP also predates this change. The [trace lifecycle documentation](LOCAL_MODEL.md#preserve-a-request-before-waiting-for-its-response) and an optional prediction exercise explain what these checks establish.

## Reach the handoff with constrained decoding, then preserve the final-response timeout

One fresh Qwen3-4B attempt used committed host `0ab07e8af6f5c213e0ebc2217b80e08fa0949e02` with both `--enforce-dependencies` and `--constrain-actions`. It completed all seven requested calls in dependency order: queue, selected context, both readiness checks, both English drafts and the recorded issue handoff. Every returned turn reports constrained generation. There were no correction requests, retries or tool errors. The host's allowed plan and IDs are visible alongside each model choice.

The next response wait reached the existing 180-second timeout. The process exited with code 1; the trace records `host_error`, `ExceptionGroup`, seven returned turns and no final answer. Captured stderr identifies the nested `TimeoutError`. A separate [terminal observation](../evidence/host-observations/qwen4-morning-constrained.json) binds that observation to raw-trace SHA-256 `6f87257d6c6eda7fdc7bf836f6f435a98d086dc0d163d813563a703d9e662b97`. The host did not persist its eighth in-flight request before awaiting the response; neither that input nor missing model text is reconstructed as observed output. The preceding thirteen raw traces remain unchanged.

The replay exposes decoding schemas and the terminal error, plus a separate link to the host observation. Regression checks reconstruct policy state from actual returns, validate each recorded action against its saved schema and compare all seven tool results with the unchanged engine. The prepared handoff still needs SDK version, observation time window and redacted logs. This establishes tool-work completion under assistance, not a completed model-written explanation. See the [per-turn timings, results and limits](LOCAL_MODEL.md#constrained-morning-workflow-seven-calls-then-a-response-timeout).

All 409 Python tests, 105 JavaScript tests and Ruff checks passed. Local browser checks confirmed seven separate returned turns, the queue-only decoding schema, the handoff's missing fields and the separate terminal-observation link. The fourteen-attempt project brief retains two pages and seven links; both rendered pages were visually inspected. These verify the replay and evidence consistency, not model reliability, customer outcomes or personal mastery.

## Constrain the next action without certifying the final explanation

The optional `--constrain-actions` mode derives a JSON schema from the morning policy's current pending work and sends it to the existing local model worker. It allows one action per turn, with IDs learned from successful results, then a final string only after all requested work. The state message explicitly asks for one action. The earlier unconstrained mode and recordings are unchanged. Parser and runtime policy validation remain in place.

All 406 Python tests and Ruff checks passed. The schema is tested with both JSON Schema validation and the installed `lm-format-enforcer==0.11.3` character parser. A seven-call fixture walkthrough checks each successive schema; separate cases cover unknown IDs, wrong argument/tool pairings, premature finals, completed work and failed calls. Real-MCP scripted-host checks verify delivery of every schema and runtime rejection when a scripted worker ignores it. The final-string schema intentionally does not evaluate factuality. These are software checks before a new model attempt, not evidence that the model completes the task. See [the decoding assistance and limits](DEPENDENCY_POLICY.md#optional-constrained-generation).

## Record what happened after enabling the dependency policy

One new Qwen3-4B morning-review attempt used committed host `f0cb1e428ec09cd6b595f2ecb4766fecb72db85a` with `--enforce-dependencies`, eight turns, 768 output tokens and no corrections. The host supplied a one-action pending queue state before generation. The model still proposed five actions, with invented account, integration and issue IDs. The existing parser rejected the batch before dependency validation. No tool executed; the policy stayed at `awaiting_queue` with one pending action and no completed work. This is a failed model-use observation, not a failure of a policy check that was never reached.

The new raw trace is preserved byte-for-byte with SHA-256 `bf65fa466c0f3acd72bb43fe0e0bfbe72ad22986b07e6ff9a477f832ee2e6c84`; the preceding twelve raw files remain unchanged. The replay now exposes the exact per-turn host state before the model's proposal, and distinguishes parser, dependency and result-check failures. Tests cover provenance, state-message escaping and those separate display boundaries. The initial-message hash matches the original morning attempt; the per-turn state message is additional model input and is disclosed separately. See the [recorded outcome](LOCAL_MODEL.md#policy-enabled-attempt-parser-stops-the-proposal-first).

All 390 Python tests, 103 JavaScript tests and Ruff checks passed. Local browser inspection confirmed the new selection, 0/7 execution, one pending queue action and the exact pre-generation host message. The refreshed project brief has two pages and seven links; both rendered pages were visually inspected. These checks verify the published explanation and replay, not model reliability or personal mastery.

## Enforce dependencies after the prompt-only attempt fails

The optional `--enforce-dependencies` flag adds a stateful policy to the morning-review batch host. It learns the selected account from a successful queue result and pending integration/issue work from successful context. Each entire proposal is checked before execution; correct-looking IDs cannot skip those dependencies. Failed calls stay pending, accepted results remove only their corresponding work, and an unfinished workflow cannot accept a final response. A malformed or mis-scoped successful result stops the remaining batch. The policy also supplies pending-action state each turn, which is explicit host planning assistance.

All 388 Python tests, 100 JavaScript tests and Ruff checks passed. The Python suite includes seven scripted-worker integration scenarios using the real MCP stdio server: a complete seven-call workflow, premature final, dependent and mixed-scope batches, a fabricated account, an injected tool error with retry, and an injected result-scope mismatch. Policy unit cases use unfamiliar IDs and cover empty work, malformed records and duplicates. These are software tests; the twelve model recordings remain unchanged and none uses this policy yet. The [design and boundaries](DEPENDENCY_POLICY.md) and [prediction exercise](LEARNING.md#optional-engineering-exercise-a-correct-id-can-still-arrive-too-early) make this a reviewable failure-to-fix learning example. Final prose still requires separate review; the fixed v0.29.8 bundle predates this implementation.

## Test a dependency instruction without claiming it enforces the workflow

An optional `--sequence-dependencies` paragraph asks the morning-review model to retrieve the queue alone, wait for account context and use only previously returned IDs. It does not change parser limits, tools or runtime validation; original default prompts remain identical. The flag and its test were committed before one new local Qwen3-4B attempt.

The model again proposed five actions before tool results. The first four proposals match the earlier attempt; the issue placeholder changes from `12345` to `11223`. Batch validation again rejected the entire response. The recorded result remains 0/7, with no final answer or corrections and no token-cap hit. A paired regression checks the exact one-paragraph system-input difference, unchanged task, tool schemas, runtime settings and limits. This is evidence that this instruction was insufficient for this attempt, not a failure-rate estimate or an implemented dependency guard.

The raw trace SHA-256 is `247be9a71ee43d8f1e925d38d411281dfa341afa4f700ed5f81668d13469de1a`. Both morning attempts are linked together in the replay, and the prior eleven raw files remain unchanged. The fixed v0.29.8 release predates both recordings.

All 344 Python tests, 100 JavaScript tests and Ruff checks passed. Local browser checks switched between both comparison links, showed their separate 0/7 results and exposed the added paragraph in the recorded system input. Both pages of the refreshed twelve-attempt project brief were rendered and visually checked. These verify published behavior and evidence consistency, not improved model performance.

## Record a queue-first task without supplied account identifiers

The earlier platform task names both integrations. A new `morning_review` task asks the model to obtain the snapshot queue, select its first account, retrieve context and prepare scoped readiness, English follow-ups and issue handoffs. Its seven expected calls are defined against the fixed fixture and tested separately from the prompt; coverage does not establish call order, ID discovery or answer quality. Task and coverage code were committed before inference.

One local Qwen3-4B attempt proposed five actions in its first response, including dependent calls with unsupported `12345` and `67890` identifiers before any tool result. The host rejected the whole batch because the maximum is four. It did not salvage the queue call or execute identifier validation. The recording ends with `invalid_action`, zero of seven requested calls observed, no final answer and no corrections. It used 97 generated tokens without reaching the cap. No retries were performed for this task.

The raw trace is retained byte-for-byte (SHA-256 `31314f78a3b14604473b80e9e3d950007ae602e7b269bf54ab2db6f455896405`) alongside the unchanged previous ten recordings. The browser shows its rejected proposal and empty execution path. The documentation describes the failed dependency plan without claiming successful account discovery. All 341 Python tests and 100 JavaScript tests passed; both PDF pages were rendered and visually checked with the new eleven-attempt count. Browser inspection confirmed 0/7, the exact batch-limit error and no executed calls. Review annotations remain AI-assisted; this is a new development failure, not an independent benchmark. The fixed v0.29.8 release predates the new task and recording.

## Keep the recorded problem visible in the terminal handoff review

The compact morning review listed issue IDs, handoff state and missing fields but omitted the recorded problem. It now includes the issue record's summary beside each platform's handoff. Harbor's review therefore says that the recorded callback returned HTTP 405 before showing missing reproduction steps and logs. The output does not substitute a draft title, diagnose the cause or establish that the symptom is still current.

Four failing-before checks cover missing, unique and duplicate handoff drafts plus Unicode text with terminal control characters and line breaks. They verify that the recorded summary stays visible, remains scoped to Android rather than appearing under iOS, does not borrow a draft title and leaves the workflow unchanged. All 335 Python tests and Ruff checks passed. Regeneration changed only the two issue lines in the committed morning summary; the full briefs and workflow data are unchanged. These are authored regression cases, not real customer incidents. The fixed v0.29.7 package predates this change.

## Make follow-up drafts usable when clipboard access fails

The follow-up copy button previously reported "Select text to copy" after failure without providing a keyboard-friendly text field. A collapsed manual-copy view now contains the exact selected draft in a labeled, read-only textarea. Clipboard failure opens it, focuses the field and selects its contents. The app assigns the draft as a textarea value; changing language or platform rebuilds the view from that selection. The existing clipboard helper suppresses late feedback from replaced controls.

Edge QA used a local server with `Permissions-Policy: clipboard-write=()` to exercise actual browser denial without changing browser permissions. The fallback selected all 621 English characters and all 237 Chinese characters for Android. Switching to iOS replaced the field with its 132-character Chinese draft; Enter, Tab and Ctrl+A also reached and selected the manual field. Each value matched the displayed draft exactly. All 100 JavaScript tests passed, including denial and stale-callback checks. This verifies these interactions and selection contents, not an external paste destination or a complete accessibility audit. The fixed v0.29.7 package predates this change.

## Attribute the model's contribution to what the recordings show

The README and interview guide now distinguish the working deterministic baseline from the model layer's intended benefit. A linked architecture table traces platform follow-up, inbound-message review and correction handling to their saved runs. Source inspection confirmed that the platform task supplies both integration IDs, the batch model proposes four readiness/draft calls, the inbound task supplies the exact messages, and the constrained run contains two correction requests before structured fields match. The first correction supplies expected evidence IDs; prose verification remains absent. This is an explanation of existing evidence, not a new baseline experiment, autonomous account-discovery result or measured productivity benefit.

## Preserve keyboard position when cancelling a practice resume

Activating **Keep current work** with Enter hid the focused button and left browser focus on `BODY`. The notes survived, but the keyboard user lost the active control. Cancellation now returns focus to the saved-file chooser. Escape within the preview uses the same cancellation path; the shortcut is scoped to that preview and described beside the replacement controls.

Edge QA reproduced the earlier focus loss, then checked Tab from the file chooser, Enter to expand a saved decision, Escape from that heading and Enter on the cancellation button. Both cancellation paths cleared the pending preview, returned focus to `practice-load` and preserved the QA draft note. Escape in the reasoning textarea left the pending preview open. All 100 JavaScript checks passed. These are specific keyboard observations, not a complete accessibility or screen-reader audit, and the QA note is not personal learning evidence.

## Inspect saved practice responses before replacing current work

The resume preview previously showed only a decision count and the selected exercise. It now adds a collapsed section for each saved decision, with the saved option and separately labeled unfinished/initial reasoning and later reflection. It uses text nodes for the saved content and does not include option feedback or policy explanations. Selection alone still does not replace the current session; the existing explicit replacement action remains required.

Local Edge checks used clearly labeled QA-only progress files outside the repository. Preview and cancellation preserved an unsaved current note, invalid JSON was rejected, Unicode and markup remained literal text, and explicit resume restored an editable unfinished note plus a separate read-only initial note and editable reflection. The preview stayed within a 320-pixel viewport; the desktop viewport was restored afterward. Reset cleared the QA session and preview. All 100 JavaScript checks passed. The file schema, exercise signature and learning content are unchanged, so existing compatible files remain usable. These checks do not represent personal practice by Yuchi or a complete accessibility audit. The fixed v0.29.7 package predates this UI change.

## Make the MCP learning exercise observable

Session 3 previously asked the learner to run and inspect the smoke transcript without specifying a fresh output path or a focused inspection sequence. It now asks for predictions, writes the real stdio result under ignored `dist/`, and provides a small inspector for available tools, successful calls, retrieved prompts, review/data timestamps and an expected-error flag. It distinguishes scripted call selection from model-proposed actions and explains why a pre-existing file cannot establish a failed run's success.

Documentation QA ran the stated command and executed the exact published Python block. It observed eight available tools, 18 successful calls, two prompts, Android's blocked result and unchanged dataset time in both queue calls. The new JSON matched the reference transcript, the inspector preserved the fixture and reference-file hashes, and Git confirmed the output path is ignored. This checks the exercise, not Yuchi's predictions, personal understanding or model reliability. No model inference was performed and no personal response was supplied.

## Clarify the request before judging technical intake in the summary

The compact terminal summary preserved `needs_scope` but paired it with generic missing-field status and omitted the issue's next action. With the same synthetic request, "Please explain invoicing.", it showed either `missing: reproduction_steps, redacted_logs` or `missing: none` after all intake fields were populated with unreviewed placeholders. The engine requested scope clarification in both cases; no triage rule changed.

Two failing-before tests now pass: the summary explicitly prioritizes scope and displays the engine's clarification action and proposed CSM owner without presenting technical completeness as the issue's next step. The full brief retains the recorded fields for inspection. Both tests use actual engine output, preserve another issue's technical handoff and leave the input unchanged. All 331 Python tests passed, and the default 1,879-byte morning summary remained byte-identical. This is a presentation correction, not a verified billing workflow, improved classification result or personal learning completion. The fixed v0.29.7 source predates this change.

## Keep ambiguous handoffs out of the terminal summary

The compact `csm-demo --format summary` output selected the first draft matching an issue. This disagreed with the browser and Markdown brief, which already withheld duplicate matches. Four failing-before regression variants reproduced the problem with identical and conflicting duplicates in both array orders.

The summary now requires exactly one matching draft before displaying its handoff state, missing fields and proposed owner. Multiple matches retain the issue ID and report the match count with a request to review the packet. Missing drafts keep their existing explicit notice. The checks also preserve readiness, a different account's valid handoff and the input packet. All 329 Python tests passed, and the normal committed 1,879-byte summary remained byte-identical. The duplicated packets are authored diagnostic cases, not defects observed in real customer data. The fixed v0.29.6 package predates this repair.

## Keep the navigation within a narrow viewport

At a 320-pixel Edge viewport, the header navigation extended to about 328 pixels and widened the page beyond its 305-pixel content area (the scrollbar occupied the remaining width). The mobile header and its navigation now allow flex wrapping. Links move onto another line when space is insufficient instead of extending past the page edge.

Browser checks at 320, 390 and 720 pixels, followed by the restored 2002-pixel desktop viewport, found document scroll width equal to document client width. At 320 pixels, Harbor's expanded queue evidence, handoff preview and field-source comparison remained within the viewport; the read-only preview had equal scroll and client widths. A targeted screenshot confirmed the wrapped header. The initial emulated full-viewport capture was incorrectly scaled by the browser capture tool, so it was not used as visual evidence. These are bounded layout checks, not a complete mobile-device or accessibility audit. The fixed v0.29.6 download predates this CSS repair.

## Bound verification waits without changing workflow results

The scripted MCP smoke client left its response timeout unset. A test peer that accepted the initialization request but never replied reached the test's outer watchdog instead of producing a protocol timeout. The client now configures the SDK's 30-second response timeout. The regression test shortens that setting to 50 ms, uses the real SDK session over in-memory streams, and verifies the timeout error and stream cleanup. This does not simulate an operating-system process hang or prove process-tree cleanup.

A fresh real stdio run completed and its JSON matched the published transcript. CI also sets a three-minute limit on the smoke step, seven minutes on isolated-wheel verification, and fifteen minutes on the full matrix job. These are failure bounds, not performance targets or measured speed improvements. GitHub's step/job cancellation remains separate from the SDK's response deadline. No test coverage was skipped and the recorded model attempts remain unchanged.

## Rehearse the evidence decisions with a small experiment

The interview guide now connects queue selection, field-source agreement and unavailable handoffs to specific review actions. An optional learning exercise asks for predictions before exposing runnable code that varies one, zero or two drafts for Lantern's recorded Android issue. Documentation QA executed the exact snippet in all three modes: the normal case retained the field comparison, the altered cases reported zero/two matches, the original packet remained equal to a fresh generated packet, and the source fixture's SHA-256 was unchanged. This verifies the teaching material; it is not a personal reflection or completed practice by Yuchi. The guide explicitly requires current source after the repair because v0.29.6 predates that export behavior.

## Do not turn ambiguous handoff packets into usable drafts

The browser withheld duplicate matching drafts, but the Markdown renderer iterated directly over the ticket list. Three failing-before tests reproduced duplicate drafts being printed, a recorded issue with no draft disappearing from the handoff section, and an unmatched draft being presented without a recorded issue.

The export now starts from recorded issue IDs and requires one matching draft. Missing or duplicate matches produce an explicit notice, retaining the issue identity and evidence index; unmatched drafts in whole-queue exports are flagged without copying their content. Selected-platform filtering excludes drafts that cannot be attributed to that platform's issues. The tests reverse duplicate order, exercise both languages and export scopes, preserve other valid handoffs, and check escaped identifiers and unchanged inputs. Existing bundled briefs remain byte-identical because their issue/draft pairing is unambiguous. These are authored packet-integrity cases, not evidence that real customer records have been validated.

## Preserve source comparisons in downloadable briefs

The Markdown briefs retained copied handoff values and source IDs but did not flag disagreements with scoped records. A missing field-source entry also raised a `KeyError` and stopped the export. Four failing-before checks covered disagreement, unavailable/ambiguous/mis-scoped sources, matching attribution and source markup.

Each handoff now includes a field-source comparison table. Configuration records remain distinct from dated issue details, unavailable sources are labeled rather than substituted, and the original copied values remain visible. The rebuilt English and Chinese briefs use the same renderer as the CLI. Full Python verification passed with 321 tests, including byte comparisons of the committed briefs. This is an export integrity repair, not independent verification of source truth or completed personal practice.

## Keep field-source warnings in portable handoffs

The on-screen handoff source view displayed a mismatch when a draft field differed from its scoped record. The plain-text copy previously retained the draft value and a source ID, but omitted that specific warning and the recorded value. Three new tests failed against that exporter before the repair: changed values, unavailable or ambiguous sources, and matching attributed fields.

Both views now use one scoped lookup. The portable handoff includes the recorded value and its source description when uniquely available, a disagreement warning when values differ, and an unavailable-source warning otherwise. It retains the draft value for comparison rather than silently correcting it. Multiline recorded values stay quoted as source text. These checks establish agreement with structured records, not source truth, semantic extraction or customer outcomes. The synthetic fixture and saved model attempts are unchanged.

## v0.27.1: keep delayed copy feedback with its original selection

A controlled replay of the previous draft click handler reproduced two asynchronous failures: resolving a copy after replacing the draft button marked the replacement as copied, and resolving after leaving the draft tab threw a `TypeError` while accessing the missing button. Share-link buttons could similarly show a late result after their selection changed.

A small shared clipboard-feedback helper now retains the originating button and an attempt token. Rendering a new share selection invalidates that button's pending feedback; a disconnected draft button cannot update its replacement. The newest attempt alone may update its control. Current failures retain the selectable-link fallback, while stale failures cannot open details or move focus. Six controlled tests exercise delayed success/failure, removal, repeated attempts, independent controls, synchronous API absence and exact text submission. This controls UI feedback; it does not cancel a clipboard write already requested or establish the clipboard's contents after other applications change them.

## Learning-guide repair: start with an experiment the fixture supports

The guide previously asked the learner to remove Meadow's device evidence, but the current fixture already has an unknown device fact with no references. That instruction did not define the intended state change. Session 2 now adds a scoped synthetic observation to an in-memory deep copy, asks for predictions before execution, and offers passing and incorrectly scoped variants. The example is runnable after normal environment setup and leaves the bundled data unchanged.

Documentation QA executed the published snippet: `not_met` produced `blocked`, `met` produced `checklist_complete`, and a record assigned to `lantern_ios` under Meadow's account was rejected during validation. Both valid runs preserved the original `needs_evidence` result, and the fixture hash was unchanged. These are agent-run checks of the teaching material, not completed practice by Yuchi. A three-step entry route now prioritizes a customer decision, an AI claim review and one personally explained experiment; the longer exercises remain optional extensions.

## v0.27: read the record behind a checklist state

The evidence table exposed source IDs, while the supporting records were available only as JSON. A new **Trace checklist decisions to source records** disclosure lets a reviewer open a check and read its cited text, full timestamp, source kind, account/platform scope and structured claim. Unknown and failed checks include the existing evidence request; uncited checks do not acquire invented evidence. Raw records remain available separately.

The view joins only on the cited ID plus the selected account and integration. Missing or incorrectly scoped records produce an explicit unavailable-source notice. Missing claims and disagreements with the displayed state remain visible; the UI never recalculates or silently repairs the engine decision. Four new JavaScript checks cover those boundaries and escaped text. This makes provenance easier to inspect without claiming independent source verification or improved AI accuracy.

## v0.26.1: keep the presenter in the case workflow

Keyboard inspection of the published v0.26.0 explorer reproduced focus loss: changing the platform or client language rebuilt the focused select, leaving `document.activeElement` on `BODY`. Selecting an account also rebuilt its button. A keyboard presenter could lose their place while comparing the very cases the interview route recommends.

Account selection now updates the existing buttons' selected state. Case rendering restores focus to a replaced platform/language control only if that control was focused before rendering, without scrolling. Other navigation retains its own focus behavior. This changes presentation behavior only; customer evidence, engine decisions and recorded model attempts are unchanged.

Local Edge checks verified Android → iOS → Android, English → Chinese, Tab to Copy draft, Enter to select an account followed by Tab to the next account, and ArrowRight/Home in the review tabs. The narrow browser check is not a screen-reader audit or a claim of full accessibility conformance.

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

## v0.27.2: preserve scope clarification in exported handoffs

For an invoicing request classified as `needs_scope`, the browser prioritized clarification, but the Markdown handoff still listed missing technical fields. With all generic fields populated, it instead said no scoped required fields were missing. Either presentation could distract from the unresolved request scope.

The export now explicitly asks for the request, desired outcome and relevant account or product before choosing an owner or collecting technical details. It retains the original report, recorded fields, source references and neutral questions. Four regression variants cover complete/incomplete intake fields with English/Chinese draft exports; they reproduced the missing scope-first presentation before the repair and pass afterward. Existing technical cases retain their missing-field requests. This aligns export wording with the existing tool state; it does not improve the classifier or establish that an invoicing request belongs to a particular billing process.

To explain the change yourself, predict the next request for an invoice question with and without a populated SDK version. Then trace `handoff_state` from the tool into the browser and Markdown renderers. Explain why field completeness and issue scope answer different questions. This is an exercise, not a record of completed personal practice.

## v0.28: inspect the source of a handoff field

The browser's field-source disclosure previously displayed only a JSON map of source kinds and IDs. Each field can now be expanded to compare its handoff value with the original structured value, identify the source and read its date when available. Integration configuration has no per-field observation date and is labeled accordingly. Issue details remain attributed to the original report; the view does not claim to extract or verify them from its wording.

Source resolution checks the issue, account and integration. Missing or ambiguous records and differing values produce review notices without overwriting the handoff. The original-message lookup also checks account ownership. Four added JavaScript checks cover provenance, unavailable or misattributed records, differing values, escaped text and source isolation. The original report and raw field-source map remain inspectable. No source truth, customer outcome or improvement in model reliability is established by this display.

## v0.28.1: resolve configuration citations inside the portable brief

App and platform handoff fields cited integration IDs, but the exported Evidence index contained only reports and test records. A reader could not inspect the original configuration row within the brief. A separate Integration record index now includes the original app/platform values and account ID for each included integration, with an explicit boundary around missing observation dates and independent verification.

Six added regression variants cover full-queue and selected-platform exports in both draft languages, source values that differ from copied handoff values, unavailable/ambiguous or mis-scoped records, escaped content and non-mutation. The tests first failed because the index was absent. Regenerating the existing briefs carries this source trail into the downloads without changing readiness, follow-up decisions or historical model recordings.

The public-download comparison also exposed a local Windows artifact difference: full-queue briefs used CRLF while the renderer, CLI, platform briefs and committed files used LF. The builder now writes LF explicitly. Two byte-level checks failed on the Windows-generated files and pass after regeneration; CI repeats them immediately after building the demo so Git's line-ending normalization cannot hide that particular mismatch.

## v0.28.2: review before resetting personal practice

The published Reset button cleared an unfinished QA note in one click. It now opens an inline confirmation whenever practice work exists. Keep my work and Escape preserve the session; the explicit clear action resets all decisions and pending imports. Focus starts on the keep action, returns to Reset after cancellation, and moves to the decision selector after clearing. Rendering a different practice view dismisses an outstanding confirmation. Blank sessions still reset immediately.

Browser verification used explicitly labeled QA notes, a reviewed answer, a later reflection and an unfinished second decision. It checked cancellation, Escape, view changes, confirmed clearing, disabled downloads after reset, keyboard focus and mobile layout. This is interface verification, not personal learning evidence. Reload behavior and the local save/resume format are unchanged.

## v0.28.3: carry recorded failures into the follow-up wording

Running the learning guide exposed that unknown and failed device evidence produced different readiness states but identical customer messages. Failed requests now state that the check was not met according to the records before asking for updated evidence. Unknown requests keep their existing wording. Both languages use this distinction; readiness rules, requested evidence, routing and contact history are unchanged.

Four regression cases first reproduced the absent distinction and then passed with the change. They cover a mixed unknown/failed message, a newly recorded failure, source references and unchanged data/queue behavior. The historical-model integrity check explicitly accounts for the one changed Android sentence and its content-derived draft ID while comparing every other field. All ten recordings retain their original tool inputs and model outputs; no inference was repeated and no model-improvement claim follows from this template change. The learning guide links the earlier observation to the new regression example.

## v0.29: inspect a request's sources beside the draft

The follow-up panel previously exposed its evidence IDs and request metadata only as raw JSON. A collapsed source view now pairs each evidence request with its checklist state, original scoped records and selected-language request text. It reuses the existing readable checklist-source renderer, so source dates, missing records and conflicting claims remain visible in both places. Only requested checks appear; a draft with no evidence requests adds no empty section.

Four JavaScript checks cover both languages, request/check mismatches and duplicate check definitions, missing draft citations, wrong-account sources, escaped text and non-mutation. Local browser checks opened the dated Android failure and the unknown approval check, switched the request language to Chinese, and confirmed that iOS launch-plan review has no evidence-request section. The feature explains why a request was assembled; it does not validate every draft sentence, establish current readiness or change any recorded model result.

## v0.29.1: withhold ambiguous source quotations

The readable checklist and original-message views used the first matching evidence record, while the handoff field view already required one unique scoped match. A deliberately duplicated record in a copied replay packet exposed that inconsistency: array order could determine which text a reviewer saw as the source. The published dataset did not contain these duplicates.

Checklist and follow-up source views now display an ambiguity notice when multiple records match the citation, account and integration. Original issue views also withhold an unavailable or ambiguous quotation. The existing checklist state and requested action remain visible; the renderer does not resolve the conflict or recalculate readiness.

Two new regression cases failed before the repair and pass afterward. They cover identical and conflicting device records, reversed array order, both draft languages, original messages in evidence and handoff views, and non-mutation. A third control confirms that an unrelated same-ID record cannot displace one uniquely matching scoped source. This is defensive rendering for malformed replay data, not evidence of production conflict resolution or independently verified source truth.

## v0.29.2: align host guidance with the workflow

The MCP initialization instructions said to distinguish unknown from missing, although missing evidence is one reason a check is unknown. They now distinguish insufficient evidence from a recorded unmet requirement. The morning prompt explicitly includes unknown-contact entries without calling them overdue, names the review and dataset dates, and requests a follow-up for each queued integration. A completed checklist therefore retains its launch-plan-review follow-up. Proposed ownership remains project policy rather than a confirmed assignment.

The scripted transport transcript now captures the actual initialization instructions and both retrieved prompt responses. This makes the guidance inspectable beside the tool results and allows the existing isolated-wheel comparison to check that the installed server delivers the same instructions. Tool rules, synthetic records and historical model recordings are unchanged. This is a guidance correction and protocol observation, not a new model run or evidence that a host follows these instructions reliably.

## v0.29.3: keep ambiguous dates out of the evidence timeline

The source quotation views required one unique scoped record, but the timing helper indexed records by ID with the last match winning. In a deliberately malformed copy of a replay packet, a duplicate could replace the displayed date. A same-ID record from another account or platform could also hide a valid source, depending on array order. The bundled dataset contains no duplicate IDs.

Timing now groups records within the selected account and integration, then requires exactly one match per citation. An ambiguous date is withheld and its ID is listed as unavailable. The exported Evidence index retains the raw records so a reviewer can inspect the conflict; the helper neither reconciles it nor changes readiness.

Ten added regression variants cover identical and conflicting duplicate dates, both array orders, unrelated same-ID records, both draft languages and unchanged input packets. Eight failed before the repair; the two reversed-order controls already passed. All pass after the repair. This aligns descriptive timing with the existing source-view boundary; it is not independent source validation or a new freshness policy.

## Keyboard presentation after v0.29.3

An Edge/Windows keyboard check confirmed that the review tabs keep selection, focus and panel labeling aligned under Left/Right Arrow, Home and End. Tab enters the follow-up language selector, and changing the language retains focus. Evidence disclosures opened with Enter or Space, including nested source headings, but their focus indicator used a thin native border while buttons and selectors used the portfolio's blue outline.

The shared focus-visible style now includes disclosure headings. Local browser checks confirmed the blue outline on both the outer follow-up evidence section and a nested checklist source. No keyboard logic or data behavior changed. The interview guide now includes the checked presentation path; no personal practice response was completed during this QA, and screen-reader behavior and other browser engines remain unverified. The fixed v0.29.3 ZIP retains its original styling.

## Put the original AI claim beside its recorded source

The three-minute review linked to the original batch attempt, but verifying its "full compliance" overstatement required opening a turn and finding the relevant tool return. The hosted explorer now places two exact excerpts beside selected fields from that same saved attempt: iOS's checklist decision and boundary, and Android's failed device status and cited record. Each pair includes the existing AI-assisted assessment, the recorded turn/call location and expandable JSON field paths. The unedited answer and complete transcript remain available below.

The replay builder extracts the values from the historical trace, without calling the current engine or a model. It requires an exact final-answer excerpt, one matching review, one successful readiness call in the requested scope and one device check where applicable. Seven added Python checks cover extraction without mutation, reordered source locations and rejection of missing quotes, duplicate calls, mismatched scope, tool errors and missing checks. A JavaScript check covers escaped text, separate review/source labels, unchanged input and recordings without comparisons. Edge checks confirmed the two-column layout, a stacked 390-pixel viewport without horizontal overflow, expandable source locations and removal of the cards when selecting another recording.

This makes an existing failure easier to inspect; it adds no inference, independent validation or automated semantic verdict. The fixed v0.29.3 package predates this presentation change. The interview guide now points to the comparison for its short AI explanation.

## Request a warning before discarding practice work

Practice now registers a native `beforeunload` warning only while a choice, nonblank note or reviewed decision exists. Clearing all work removes the listener. Downloads do not disable it: a download request cannot establish that the user retained the file. The page and practice guide explain that browsers may suppress the warning and that it does not save work.

The 21 practice and checkpoint checks pass. In the controlled Edge session, a temporary QA-only note downloaded to a local progress JSON file, reset cancellation retained the note, and confirmed reset followed by reload produced a blank session with downloads disabled. Reload and normal link navigation did not expose a native dialog in that session; visible warning behavior therefore remains unverified. No personal learning response was completed, and no automatic storage or model call was added. The immutable v0.29.4 ZIP predates this change.

## Copy one issue's handoff for review

The follow-up panel already offered a copy action, but taking a technical handoff away required downloading the full platform brief. Each available issue draft now has a plain-text copy and readonly preview. The copy preserves source attribution, recorded fields, missing intake requests, proposed ownership, unconfirmed cause, fixed snapshot and unsent status. Scope-first cases retain clarification before technical intake; ambiguous duplicate drafts are withheld rather than selected by array order.

Five added JavaScript checks cover the actual Harbor fixture, per-issue isolation and unavailable sources, scope-first behavior, ambiguous draft order, and literal text inside the preview. The existing clipboard helper supplies completion feedback and selection-safe failure handling. Edge checks observed the preview, a successful-copy label, account-specific replacement and no copy action for the issue-free iOS case. The browser-control tool's separate virtual clipboard did not expose the page's clipboard write, so clipboard payload read-back was not independently verified. No inference, issue submission or source-record change was added. The immutable v0.29.4 ZIP predates this feature.

## Preserve unknown contact history and passed planned dates in the queue

The engine already returns explicit contact and launch states, but the browser interpolated the numeric day fields directly. A copied dataset with Meadow's contact references removed and its planned launch set 30 seconds before the snapshot produced `contact_state=unknown`, `days_since_contact=null`, `days_to_launch=-0.0` and `launch_overdue=true`. Running the actual queue-rendering function with that engine output in an isolated DOM sink reproduced `Contact nulld ago` and `Launch in 0d`. An actual `include_live=True` selection for Pine produced `Launch in nulld`. These are scratch probes; the default three-account queue has recorded contacts and future planned dates.

The renderer now distinguishes unknown history, a passed planned date, an imminent rounded-zero date and a recorded live stage. It uses the engine's exact overdue flag when rounding hides the sign. A live-stage label describes the record rather than independently confirming a launch. The queue heading now says Review queue, launch countdowns are explicitly planned, and the caption explains rounding and snapshot limits. Longer labels wrap within the cards.

Four regression checks cover the bundled normal case without mutation, unknown/unavailable contact ages, overdue versus future rounded zero, and live or unavailable launch timing. Replaying the same captured engine outputs through the updated renderer produced `Contact history unknown`, `Planned date passed (<0.01d)` and `Recorded as live`. Queue selection, order, underlying dates, contact history and customer records are unchanged. These checks establish display behavior, not refreshed customer information. The fixed v0.29.5 package retains the earlier labels.

## Trace queue selection to account contact evidence

The queue showed contact age while its underlying account-level contact text was mainly available in raw data and exported evidence indexes. A collapsed source view below the account heading now places the queue rule, reported timing and account plan beside the referenced contact records. It requires a unique account-scoped contact source and keeps missing or ambiguous records unavailable. It does not recompute the selection or treat a draft, technical test or unreferenced newer record as a contact event.

Six added JavaScript checks cover the bundled evidence without mutation, unknown history, missing/duplicate/mis-scoped sources, irrelevant newer and other-account records, mismatched account context and escaped text. Edge checks confirmed Lantern's contact evidence remained open across platform, review-tab and language changes. Selecting Harbor closed the disclosure, replaced the source with `contact_acc_006` and removed Lantern's record. The fixed v0.29.5 package predates this display. No customer records, queue rules or model recordings changed.
