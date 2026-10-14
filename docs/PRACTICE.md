# Practice the decisions, then explain your reasoning

[Open the interactive practice](https://yuchi-wang02.github.io/csm-copilot/#practice).

This exercise turns five existing project decisions into a conversation about customer-success judgment. It is self-directed practice with published guidance, not a blinded test, hiring assessment, certification, or measurement of personal mastery. The application compares selected options with the project policy; it does not grade written reasoning.

## Five decisions

| Decision | Evidence used | What to explain |
|---|---|---|
| Android after two new confirmations | The actual counterfactual engine output in `workflow.counterfactual.after` | Why a failed device check needs a retest while an unknown callback check needs evidence |
| iOS after checklist completion | Lantern iOS readiness and English follow-up from the workflow packet | Why the next action changes to launch-plan review without approving launch |
| Model fields after two corrections | The published `qwen4-constrained` recording and its response review | Why matching fields do not certify the model's prose or establish general accuracy |
| Callback handoff with details already supplied | Harbor's original issue record, known fields and missing-field list | How to acknowledge known facts, request unresolved details and avoid a premature diagnosis |
| Customer intent disagrees with the tool | The preserved `not_failing` probe: customer text, current callback candidate, route and questions | Why to clarify invoicing instead of blindly sending callback questions or claiming verified callback health |

The displayed evidence comes from the same artifacts used by the case explorer and model replay. Option wording and explanations are authored teaching material based on the project's operating policy. They are not official vendor training or independently validated assessment items. Automated checks detect changes to the key fixture conditions on which these lessons depend.

## Use it before an interview

1. Read the evidence and choose a next action. Write a short reason in your own words before revealing the guidance.
2. Select **Compare with the evidence**. Your original choice and note become read-only within this session. The application explains the selected option and the project policy.
3. Write what you would change, what you would ask the customer, or what you would investigate next in the separate reflection field.
4. Switch between decisions using the selector. Your notes remain available while the page stays open. The evidence links open the relevant platform or updated comparison within the page; returning to Practice retains your notes.
5. Download the Markdown notes at any stage after choosing an option or entering a note. Unreviewed choices and reasoning are saved as editable drafts with no option comparison or guidance included for those decisions. Reviewed decisions retain the original response, published guidance and later reflection separately. The file is a readable record; it cannot restore the browser session.

The original choice is preserved to make a change in reasoning discussable. This is a convenience for reflection, not tamper-proof evidence: users can reset, reload, inspect the answer in public source, or edit a downloaded file. There is no identity check or claim that the work was completed unaided.

## Discuss the learning, not a score

After doing the exercise yourself, use a specific observation:

> “My first interpretation was ____. The record ____ changed my view because ____. I would now ask the customer ____ and keep ____ unresolved until we have evidence.”

For the AI case, distinguish the four successful tool actions, the rejected structured responses, the assisted correction, and the remaining omissions in the explanation. Explain how a system can help the reviewer without claiming to replace their judgment.

Completing the interface alone does not prove that you understand the code. Pair your reflection with one source trace, a test you can explain, and a small change you personally implement and verify. Keep any later human review or personal contribution clearly dated and separate from this AI-assisted implementation.

## Data and verification

Practice notes are held only in page memory. There is no note upload, model call, analytics event, browser storage, or backend persistence in the practice feature. Reloading or resetting clears them. Downloading creates a local file that you decide whether to share. As with other parts of the site, hosting and the optional font request may generate ordinary network traffic; practice notes are not included in those requests.

The interface uses native radio inputs and labeled text areas. Revealing guidance moves keyboard focus to the feedback. The downloadable report quotes and escapes user-authored notes so they cannot inject active HTML or report headings.

Evidence labels, values and source IDs are also escaped in the Markdown download. A customer message's formatting remains source text instead of becoming a heading, HTML element or authored Markdown link in the report. Evidence line breaks are flattened for the list; your own notes retain quoted line breaks. Escaping changes the file's Markdown syntax, not the stored source record.

Run `node --test tests-js/practice.test.cjs` with Node 24. The fifteen checks cover fixture grounding, valid choices and preserved initial work, reviewed and unfinished report content, note escaping, a clean reset, pre-guidance export availability, the exact model-recording link, the callback exercise's source grounding and reflection export, literal-text handling for evidence labels, values and source IDs, and the fifth decision's preserved failure, direct probe link and separate draft/reflection export. GitHub CI runs these alongside the Python suite on Windows and Ubuntu. They verify application behavior, not learning outcomes.

## Save unfinished work

You do not have to reveal guidance to save your reasoning. A choice without a note, a note without a choice, or a mix of reviewed and unfinished decisions can be downloaded. Blank sessions keep the download disabled. Saving does not reveal an answer, mark an item reviewed, freeze an unfinished draft or claim a completed exercise. Reload still starts a new browser session; keep the Markdown file if you want to return to your reasoning later.

The model exercise links directly to `qwen4-constrained`, the recording its evidence describes. It does not depend on which model attempt was most recently added to the portfolio.

## Question a tool recommendation

The fifth decision uses an actual remaining mismatch in the published triage probes. Before you reveal guidance, the page shows only the customer message and tool result, without the authored expected category. Afterward, its evidence link opens that exact probe and the raw output while retaining your notes. The baseline still fails this wording; adding an exercise does not repair the classifier or improve its diagnostic score.

Explain the distinction between what a customer reports, what a tool retrieves, and what has been independently checked. Draft a reply that acknowledges the invoice request and asks for the missing account or invoice context. Do not infer a Finance owner, invoice defect, service deadline or verified callback health from this record.

## Open the decision you want to discuss

Each decision has a public copy button and a selectable link fallback. For example, [open the tool-disagreement exercise directly](https://yuchi-wang02.github.io/csm-copilot/?practice=question_triage#practice). Shared links select only the exercise; they do not include your choices, notes or guidance state. Back and Forward retain work within the loaded page, while reload starts a fresh session. See [all five direct links and navigation rules](SHARING.md#share-a-practice-decision).
