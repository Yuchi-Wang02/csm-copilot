# Practice the decisions, then explain your reasoning

[Open the interactive practice](https://yuchi-wang02.github.io/csm-copilot/#practice).

This exercise turns six existing project decisions into a conversation about customer-success judgment. It is self-directed practice with published guidance, not a blinded test, hiring assessment, certification, or measurement of personal mastery. The application compares selected options with the project policy; it does not grade written reasoning.

## Six decisions

| Decision | Evidence used | What to explain |
|---|---|---|
| Android after two new confirmations | The actual counterfactual engine output in `workflow.counterfactual.after` | Why a failed device check needs a retest while an unknown callback check needs evidence |
| iOS after checklist completion | Lantern iOS readiness and English follow-up from the workflow packet | Why the next action changes to launch-plan review without approving launch |
| Model fields after two corrections | The published `qwen4-constrained` recording and its response review | Why matching fields do not certify the model's prose or establish general accuracy |
| Callback handoff with details already supplied | Harbor's original issue record, known fields and missing-field list | How to acknowledge known facts, request unresolved details and avoid a premature diagnosis |
| Customer intent disagrees with the tool | The preserved `not_failing` probe: customer text and the recorded before-repair callback candidate, route and questions | Why to clarify invoicing instead of blindly sending callback questions or claiming verified callback health |
| Citation identity versus purpose | The original `qwen4-morning-field-review` answer, issue report, readiness sources and handoff attribution | Why one real, correctly scoped source can support a handoff detail without supporting the readiness claim beside it |

The displayed evidence comes from the same artifacts used by the case explorer and model replay. Option wording and explanations are authored teaching material based on the project's operating policy. They are not official vendor training or independently validated assessment items. Automated checks detect changes to the key fixture conditions on which these lessons depend.

## Use it before an interview

1. Read the evidence and choose a next action. Write a short reason in your own words before revealing the guidance.
2. Select **Compare with the evidence**. Your original choice and note become read-only within this session. The application explains the selected option and the project policy.
3. Write what you would change, what you would ask the customer, or what you would investigate next in the separate reflection field.
4. Switch between decisions using the selector. Your notes remain available while the page stays open. The evidence links open the relevant platform or updated comparison within the page; returning to Practice retains your notes.
5. Download the Markdown notes at any stage after choosing an option or entering a note. Unreviewed choices and reasoning are saved as editable drafts with no option comparison or guidance included for those decisions. Reviewed decisions retain the original response, published guidance and later reflection separately. The file is a readable record; it cannot restore the browser session.
6. To continue later, open **Save or resume practice progress** and select **Save progress file**. This downloads a separate JSON file. On a later visit, choose that file, review the preview, then select **Replace current work and resume**. Choosing a file alone does not replace any work. **Keep current work** cancels the preview.

The original choice is preserved to make a change in reasoning discussable. This is a convenience for reflection, not tamper-proof evidence: users can reset, reload, inspect the answer in public source, or edit a downloaded file. There is no identity check or claim that the work was completed unaided.

## Discuss the learning, not a score

After doing the exercise yourself, use a specific observation:

> “My first interpretation was ____. The record ____ changed my view because ____. I would now ask the customer ____ and keep ____ unresolved until we have evidence.”

For the AI case, distinguish the four successful tool actions, the rejected structured responses, the assisted correction, and the remaining omissions in the explanation. Explain how a system can help the reviewer without claiming to replace their judgment.

Completing the interface alone does not prove that you understand the code. Pair your reflection with one source trace, a test you can explain, and a small change you personally implement and verify. Keep any later human review or personal contribution clearly dated and separate from this AI-assisted implementation.

## Data and verification

Practice notes are held only in page memory unless you explicitly download them. There is no note upload, model call, analytics event, automatic browser storage, or backend persistence in the practice feature. Reloading or confirming a reset clears the in-page session. Downloading creates a local file that you decide whether to share. Resuming reads the file locally; it does not submit it to a service. As with other parts of the site, hosting and the optional font request may generate ordinary network traffic; practice notes are not included in those requests.

The interface uses native radio inputs and labeled text areas. Revealing guidance moves keyboard focus to the feedback. The downloadable report quotes and escapes user-authored notes so they cannot inject active HTML or report headings.

Evidence labels, values and source IDs are also escaped in the Markdown download. A customer message's formatting remains source text instead of becoming a heading, HTML element or authored Markdown link in the report. Evidence line breaks are flattened for the list; your own notes retain quoted line breaks. Escaping changes the file's Markdown syntax, not the stored source record.

Run `node --test tests-js/practice.test.cjs tests-js/practice-session.test.cjs` with Node 24. The seventeen core checks cover fixture grounding, valid choices and preserved initial work, reviewed and unfinished exports, escaping, clean reset, source links, and the six decisions' key evidence and reflection boundaries. Eight checkpoint checks cover mixed-state round trips, stable IDs, changed content, invalid files, Unicode/markup, asynchronous save capture and additive compatibility with a frozen v0.30.0 QA file. GitHub CI runs these alongside the Python suite on Windows and Ubuntu. They verify application behavior, not learning outcomes.

## Save unfinished work

You do not have to reveal guidance to save your reasoning. A choice without a note, a note without a choice, or a mix of reviewed and unfinished decisions can be downloaded. Blank sessions keep both downloads disabled. Saving does not reveal an answer, mark an item reviewed, freeze an unfinished draft or claim a completed exercise. Reload still starts a new browser session. Keep the Markdown file for reading and the progress JSON file for resuming.

## Resume without rewriting the learning record

The progress file stores only decision IDs, selected option IDs, notes, guidance-revealed state and the selected decision, alongside the evidence-snapshot date and a SHA-256 signature of the saved exercise content. The signature checks compatibility, not authenticity. Case and option reordering remains compatible. When the current catalog adds decisions, the loader compares the signature with the current content of the saved decisions and adds the new ones blank. Changes to a saved decision's evidence, option wording, policy or prompt still require keeping the old file as a separate record. Imported files cannot supply new evidence, guidance, source links or executable content.

Validation requires a nonempty set of unique, currently supported saved decisions, allowed option IDs, consistent original/reviewed state, text notes of at most 4,000 characters, and a file no larger than 512 KiB. The saved selected decision must belong to that saved set. A rejected file leaves the current session unchanged. A valid file first opens a preview and replacement notice; applying it replaces the whole in-page session rather than merging potentially conflicting notes. Save current work before replacing it. Confirming reset also cancels any pending import.

For a compatible five-decision v0.30.0 file, the preview reports **5 saved · 1 added blank** and labels the citation-purpose exercise **New blank decision**. Original choices, reasoning, reviewed states and later reflections remain intact. The new decision receives no choice, note, guidance or reflection. Saving again writes all six current decisions. A six-decision file cannot resume in the older fixed v0.30.0 application; keep the original file if you also use that release. The application does not rewrite the imported file on disk.

The preview lists saved and newly added decisions in expandable sections. Inspect the saved option, unfinished or initial reasoning, and any later reflection before choosing whether to replace the current session. Empty choices and notes are labeled explicitly. The preview uses the current compatible decision titles and option text; it does not display policy feedback or reveal guidance for unfinished work. Saved notes are rendered as literal text, including line breaks and markup. Cancelling or resetting clears the preview. This is a way to inspect a local file, not proof that its saved review states or authorship are authentic. The file format and signature algorithm are unchanged; the loader now accepts a matching saved subset when the catalog adds decisions.

For keyboard review, Tab from the file chooser to the saved decision headings and use Enter or Space to expand them. **Keep current work**, or Escape while focus is inside the preview, cancels the pending resume and returns focus to the file chooser. Current answers and notes remain unchanged. Escape elsewhere on the page does not cancel this preview. After an explicit replacement, focus moves to the practice decision selector.

## Review before clearing practice

When any choice, nonblank reasoning or reviewed decision exists, **Reset all practice and clear notes** opens a confirmation without changing the session. Keyboard focus moves to **Keep my work**. That button or Escape closes the confirmation and returns focus to Reset. **Clear all practice work** clears the choices, original notes and later reflections across all six decisions, cancels pending imports and returns to the first decision. Existing downloaded files are unaffected.

Changing the practice decision, revealing guidance or applying a saved session dismisses an open reset confirmation, so it does not remain attached to a newly rendered view. A blank session resets immediately. This confirmation applies to the Reset control.

While practice work exists, the page also requests the browser's native warning before reloading or leaving. Choose the browser's stay/cancel option to retain the current page, then save a progress JSON file if you want to resume later. Leaving still discards the in-page session. The warning remains active after a download request because the page cannot confirm that you kept the file. Clearing all work removes the warning; switching between sections or decisions within the page does not invoke it.

Browsers control the wording and availability of this warning, usually require prior interaction, and may suppress it. It does not protect against a crash or forced shutdown and does not save anything automatically. Keep a progress file rather than relying on the warning.

The restored page and its Markdown export disclose that the session came from an editable local file. An imported "before guidance" label describes saved state; it does not establish actual timing, authorship, unaided work or mastery. You can still revise unfinished drafts and add later reflections, while reviewed initial responses remain read-only in the interface. No grading, certification or identity verification is added.

The model exercise links directly to `qwen4-constrained`, the recording its evidence describes. It does not depend on which model attempt was most recently added to the portfolio.

## Question a tool recommendation

The fifth decision uses an actual recorded mismatch from before the present-tense denial repair. Before you reveal guidance, the page shows only the customer message and tool result, without the authored expected category. Afterward, its evidence link opens that exact probe and the raw output while retaining your notes. The current baseline now handles this specific wording. The exercise preserves the original output and links to the before/current comparison; it does not present that historical result as current behavior. See [the failure and bounded repair](CALLBACK_HEALTH.md).

## Match a source to its purpose

The sixth decision shows the original issue report, the model's Android readiness citations, the sources attached to the recorded readiness checks, the failed-device source and the handoff fields attributed to the report. It does not reveal the checker verdict before guidance. Explain which use is supported and why matching an ID, account and platform is insufficient by itself. This teaches a claim-specific review, not a blanket rule that customer reports cannot be evidence. [Open the citation-purpose decision](https://yuchi-wang02.github.io/csm-copilot/?practice=citation_purpose#practice). This exercise and additive resume support postdate the fixed v0.30.0 package.

Explain the distinction between what a customer reports, what a tool retrieves, and what has been independently checked. Draft a reply that acknowledges the invoice request and asks for the missing account or invoice context. Do not infer a Finance owner, invoice defect, service deadline or verified callback health from this record.

## Open the decision you want to discuss

Each decision has a public copy button and a selectable link fallback. For example, [open the tool-disagreement exercise directly](https://yuchi-wang02.github.io/csm-copilot/?practice=question_triage#practice). Shared links select only the exercise; they do not include your choices, notes or guidance state. Back and Forward retain work within the loaded page, while reload starts a fresh session. See [all six direct links and navigation rules](SHARING.md#share-a-practice-decision).
