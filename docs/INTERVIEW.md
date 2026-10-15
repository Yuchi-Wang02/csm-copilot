# A three-minute walkthrough

**One customer decision, one AI mistake, one next learning step.** Use the five short speaking blocks below as a rehearsal draft. The timings are a proposed pacing plan, not a measured presentation duration or evidence that personal practice is complete. Adapt the first-person wording to what you can explain yourself.

Before presenting, open [Android evidence](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en#workspace) and [the original AI recording](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-batch#model-runs) in separate tabs. Keep the [two-page PDF brief](../demo/project-brief.pdf) available as a backup. The [on-page review route](https://yuchi-wang02.github.io/csm-copilot/#start) lets the interviewer explore independently afterward.

## 0:00–0:30 — Explain the customer problem

**Show:** Android evidence. Point to the synthetic-data and snapshot labels; stay with Lantern Games for the customer story.

> I chose a CSM onboarding problem: a publisher wants to launch, but the available evidence is incomplete. This prototype helps prepare the next customer question and technical handoff. All accounts are synthetic, so the demonstration shows workflow reasoning rather than customer impact.

## 0:30–1:10 — Show the evidence boundary

**Show:** Expand **Trace checklist decisions to source records**, then **Non-test device verification**. Compare its failed record with the unknown currency-approval check. Keep platform switching for a follow-up question.

> Android has a recorded failed device check, while currency approval is unknown. Those states need different actions: request a fresh test for the failure and confirmation for the missing evidence. Every check belongs to a specific app and platform. An iOS result cannot establish Android readiness.

## 1:10–1:50 — Move the work forward

**Show:** Open **Follow-up**, then **Handoff** in the same Android panel. Point to one specific request and one missing handoff field; do not read the entire draft aloud.

> The follow-up turns those gaps into specific requests. The handoff keeps recorded details and makes missing fields visible, including the SDK version and logs. A CSM can review and shorten the wording before using it. Generating this draft sends nothing and does not update the last-contact record.

## 1:50–2:30 — Explain the AI architecture and failure cases

**Show:** Switch to the original AI recording. In **Check the claim against the recorded result**, compare “iOS's full compliance” with the recorded `checklist_complete` decision and its scope boundary. The adjacent Android example distinguishes a recorded failure from missing evidence. Use the expandable field locations or the full turn transcript for a follow-up question; leave the corrected attempt for a deeper discussion.

> The MCP server gives a model tools to inspect the workflow. Checklist decisions remain deterministic. In this recording, the model completed four requested calls but described a scoped iOS checklist as full compliance. Successful tool use did not make its explanation faithful. This browser replays saved outputs; it does not run live inference.

## 2:30–3:00 — Explain the learning direction honestly

**Show:** Return to the customer example or leave the AI failure visible. Finish the story before opening another feature.

> I selected the project direction and used substantial AI assistance for implementation. The learning path asks me to trace a customer decision to its evidence, explain an AI mistake, and change one input in a copied dataset. I would demonstrate that understanding with my own prediction, output and explanation.

**Stop here and invite a question.** After completing the exercises yourself, replace the proposed learning step with one specific result you can explain and show. A test count or this script does not establish personal mastery.

## If there is only time for a short introduction

Use this without opening the site, then offer the [PDF brief](../demo/project-brief.pdf). Rehearse it in your own words; no speaking duration has been measured.

> CSM Copilot explores how AI can help move an onboarding account forward when the evidence is incomplete. Its MCP tools support readiness checks, bilingual drafts and technical handoffs. The demo distinguishes a failed check from missing evidence and shows an actual recorded AI response that overstates a checklist result. I selected the direction and used substantial AI assistance to implement it. The project gives me concrete decisions and failure cases to explain, with synthetic data and reproducible checks rather than a claim of production impact.

## Present with the keyboard

Use Tab to move between controls; the blue outline shows the focused control, including expandable evidence sections.

- In **Review steps**, Left/Right Arrow switches tabs and wraps at either end. Home selects Evidence; End selects Handoff. Focus remains on the selected tab.
- From **Follow-up**, Tab enters the **Client language** selector. Changing language keeps focus on that selector so you can continue to Copy draft and the evidence disclosures.
- **Select draft text manually** exposes a read-only field for the selected platform and language. Tab into it, then use Ctrl+A / Command+A and copy. If **Copy draft** cannot access the clipboard, this section opens and selects the text automatically; nothing is sent.
- Use Enter or Space on a disclosure heading to expand or collapse it. Tab then reaches the controls inside an expanded section, including nested source headings.
- In the saved-practice preview, Tab reaches each saved decision heading. Escape from inside that preview, or **Keep current work**, cancels the pending resume and returns focus to the file chooser without replacing current notes.

This path was checked in Edge on Windows. It is a presentation aid, not a screen-reader or cross-browser accessibility assessment. The current [fixed interview package](INTERVIEW_BUNDLE.md) includes the disclosure outline; older packages may predate it.

For a deeper engineering question, open the [longer-budget morning run](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-long-budget#model-runs). It completes seven calls and returns an answer, but the excerpt comparison shows a recorded failed device check described together with missing approval evidence. Explain why the schema and dependency policy permit that wording, identify the correct handoff fields in the adjacent comparison, and distinguish a runtime improvement from a faithful answer. The final generation took 272.986 seconds; this is a recorded development observation, not a production performance claim.

For the next failure-to-fix step, open the [morning field-review attempt](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-field-review#model-runs). The answer now separates unknown and failed checks, but the host rejects an issue report included among readiness citations. Explain why a real source on the correct platform can still serve the wrong evidentiary purpose. Show the exact final contract as host assistance, the single mismatch and the unedited explanation. No correction was attempted; the result is a useful rejection, not a successful final answer or evidence of independent self-correction.

## Optional deeper walkthrough

Open this only after the short story, or use it to prepare for a longer conversation. Choose one customer, AI or evaluation branch relevant to the interviewer's question; it is not part of the three-minute pacing plan.

<details>
<summary>Inspect additional customer cases, AI corrections and evaluation limits</summary>

### More detail: Explain the customer problem

“I wanted to explore how AI could support customer onboarding while keeping the CSM accountable for the next step. In this example, a publisher wants to launch on Friday. iOS looks ready, but Android shows a blank offerwall. The challenge is to turn incomplete information into a useful follow-up without overpromising.”

Open the [case explorer](https://yuchi-wang02.github.io/csm-copilot/). Point out the fixed snapshot and synthetic data label.

The download links above the queue provide a portable review brief with findings, drafts, next actions and evidence. Use it as a leave-behind or backup when you cannot run the live demo.

For a single example, use the selected-platform brief links inside the case panel. Harbor's Android export includes its callback handoff; Lantern's iOS export keeps the launch-plan review separate from Android's failed test. Both retain the original snapshot and offer English or Chinese customer drafts.

### More detail: Show the evidence boundary

Select Lantern Games. Show Android's unknown currency approval and failed device check. Switch to iOS and back.

“The checklist is scoped to the app and platform. Passing on iOS does not prove Android is ready. I also separate an unknown state from an observed failure, because they lead to different customer questions.”

Open a source link or evidence record. Explain the difference between a documented product condition and a project operating policy.

Expand **Trace checklist decisions to source records**, then **Non-test device verification**. Read the original synthetic record and its date alongside the recorded claim. Compare it with **Platform currency approval**, which has no cited record and asks for confirmation. Switch to iOS and inspect its own device record. Explain why a readable source trail establishes provenance, not independent truth or current readiness. The raw JSON remains available for deeper inspection.

### More detail: Move the work forward

Open Follow-up, switch to Chinese, then open Handoff.

“The draft asks for the missing evidence. The handoff includes what we know and makes missing fields visible. Neither action sends a message or updates the last-contact timestamp. The next owner can see what still needs to be collected.”

For a concrete handoff discussion, open [Harbor's callback case](https://yuchi-wang02.github.io/csm-copilot/?case=harbor_android&view=handoff&lang=en#workspace). Expand **Original issue record**, then compare it with **Questions to review before handoff**. The report already supplies self-managed currency, HTTP 405 and a time window. Explain which generic questions you would shorten or remove and which missing evidence you would still request. Treat the endpoint-method mismatch as a possibility to investigate. The selected-platform Markdown download carries the same report, questions and hypothesis note.

For an optional triage demonstration, open the [repaired English denial](https://yuchi-wang02.github.io/csm-copilot/?probe=callback_denial_en#triage-review), then compare the [separate positive callback](https://yuchi-wang02.github.io/csm-copilot/?probe=separate_callback#triage-review) and [remaining quoted-topic failure](https://yuchi-wang02.github.io/csm-copilot/?probe=quoted#triage-review). Explain the excluded occurrence, the separate positive symptom that survives, and the unsupported wording that still fails. The comparison uses inspected development examples and authored expectations; do not present its matches as independent accuracy.

Show the counterfactual update. Two settings change, but the failed device check remains unresolved. The expanded evidence-timing view shows the new customer confirmation beside the older device record. Explain why a recent message does not prove a fresh device test, and why age alone does not automatically expire evidence.

### More detail: Explain the AI architecture and failure cases

“The server exposes MCP tools so a model-enabled host can orchestrate the workflow. Dates and checklist rules stay deterministic. This website replays engine outputs and separately recorded local model attempts. The initial batch attempt chose all four requested calls but overstated the evidence. The constrained attempt matched structured fields after two recorded corrections; its prose still needs review. I distinguish tool coverage from answer fidelity.”

Show the original 14/18 result and the current 16/18 replay after rule adaptation. Explain that inspected negation failures informed the change, so this is not a fresh holdout. Indirect wording still fails; the separate denial probes preserve additional counterexamples. For the AI-specific extension, open [the four-call recording](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-batch#model-runs): it completed four tool calls but overstated the evidence in its final response. Explain why successful tool use and faithful summarization need separate checks.

Use **How this recorded AI run unfolded** to explain who did each part. Expand Turn 1 for the model's proposed actions and actual MCP tool returns, then Turn 2 for the unsupported final explanation. In the [constrained attempt](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-constrained#model-runs), Turns 2 and 3 show host rejection and the exact correction feedback; Turn 4 matches structured fields while prose remains unverified. Explain why expected values supplied by the host make this assisted recovery. The initial messages and original raw trace remain inspectable within the same view.

For a customer-communication alternative, open [the original inbound-message recording](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-triage-scope#model-runs). The model uses the right input text and different routes, but its invoice questions repeat a generic troubleshooting template. Discuss what you would ask instead and distinguish a proposed question from an invented company billing procedure. Then open [the neutral-question recording](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-triage-neutral-questions#model-runs) to inspect the observed change. The review is AI-assisted; no customer usefulness score is claimed.

For an engineering follow-up, open [the policy-enabled morning attempt](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-enforced#model-runs). Expand Turn 1 and **Read the exact host state message**. The host permits one queue call; the model proposes five actions anyway. Explain why the parser stops first, why the dependency policy has not been exercised by this particular proposal, and why passing the separate software tests does not mean the model completes the task. This is a concrete fix-and-retest story with an unresolved outcome, not a successful autonomous-agent demonstration.

Then open [the constrained morning workflow](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-morning-constrained#model-runs). Show the seven actual calls, expand a returned turn's generation schema, and inspect the handoff's three missing fields. Explain that the host restricted the available choices and the tools prepared the drafts. The final answer timed out, so the 7/7 count establishes completed tool work rather than a complete or faithful model-written explanation. The separate terminal-observation link preserves what the process reported without rewriting the raw trace.


### More detail: Explain the learning direction honestly

“The project connects my interest in business analytics, customer communication and process controls. I used substantial AI assistance for implementation. My next learning goal is to trace each tool, explain the tests, and implement a small improvement that I can defend myself.”

Replace the last sentence only after completing and documenting the relevant exercises. Do not claim personal implementation of a component you cannot explain.

</details>

## Questions to prepare for

| Interviewer question | A defensible answer |
|---|---|
| Why MCP? | It gives model-enabled clients a typed interface to a reusable workflow; it is not itself the language model. Use [Session 3](LEARNING.md#session-3--understand-the-mcp-boundary-45-minutes) to inspect a fresh scripted transcript and explain who selected its calls. |
| What does the model add to a workflow that already runs without it? | It explores natural-language tool orchestration and explanation. The deterministic baseline already computes states and drafts. The recorded task supplies integration IDs, and no comparison establishes better customer outcomes or lower effort. Show [the division of work](ARCHITECTURE.md#what-the-model-layer-contributes), then explain one unsupported model claim. |
| Why not let the LLM decide readiness? | Evidence state and scope should remain inspectable; the model can explain them without silently changing the rule. |
| Is this production-ready? | No. It lacks real CRM integration, auth, conflict resolution, freshness policy and human outcome validation. |
| What did you measure? | Synthetic category-set retrieval and workflow behavior; not time savings or customer success outcomes. |
| How do you know a draft is factual? | Its template is tied to structured records, but regex lint is insufficient for arbitrary model rewrites. Human claim-to-evidence review remains necessary. |
| Why is this account in the queue? | Expand **Why this account is in the queue**. The bundled review excludes recorded live accounts, includes contacts older than three days and unknown contact histories, then orders accounts by their exact planned launch time. Unknown history does not establish elapsed time, and priority is not a predicted customer-risk score. |
| If a copied field matches its source, is it verified? | It agrees with that scoped structured record. The record may still be wrong or outdated. In [Harbor's handoff](https://yuchi-wang02.github.io/csm-copilot/?case=harbor_android&view=handoff&lang=en#workspace), compare the copied value, recorded value and dated attribution, then state what external confirmation is still needed. |
| What happens when the handoff data is incomplete or contradictory? | Missing and duplicate matching drafts produce an unavailable-draft notice; the recorded issue remains. The current export also withholds unmatched draft contents. Use [the small handoff experiment](LEARNING.md#trace-a-missing-or-duplicated-handoff) to explain this behavior from an output you have reproduced yourself. |
| How would you explain the issue to a new publisher? | Start with the customer's question, distinguish the recorded Android failure from unknown settings, and ask for focused evidence. Use the [teaching example](CLIENT_EDUCATION.md) to rehearse that explanation in your own words. |
| What would you improve first? | Independent cases and human review of model-written claims, then semantic retrieval compared fairly to the baseline. |
| Can the model start from the queue without being given account IDs? | Both [queue-first attempts](LOCAL_MODEL.md#queue-first-morning-review-first-recorded-attempt) failed before execution, including the one with explicit dependency guidance. I can compare the prompt change with the unchanged rejection and explain the difference between an instruction and an enforced call policy. Successful queue-first orchestration remains unshown. |

## Portfolio wording

For a Product-focused interview, add a one-minute extension: open [Product feedback](https://yuchi-wang02.github.io/csm-copilot/#feedback), compare the two device-verification accounts, and explain why a failed test and a missing record lead to a question rather than a defect claim. The [exercise](PRODUCT_FEEDBACK.md) covers account deduplication and applicable denominators.

Safe current description:

> Developed an AI-assisted portfolio prototype of an evidence-grounded CSM onboarding workflow, with an eight-tool MCP server, bilingual follow-up templates, an interactive case explorer, and reproducible synthetic diagnostics that expose failure modes.

Avoid adding production adoption, customer impact, measured efficiency gains or independent human evaluation without new evidence.

## v0.6 demonstration exercise

Open [the constrained JSON and field-review attempt](https://yuchi-wang02.github.io/csm-copilot/?run=qwen4-constrained#model-runs). Explain the initial source-role error and repeated platform entries, then show the two correction requests and final matching fields. Expand the system-rendered evidence summary. Identify why it is different from the model explanation, and find the missing inline citations and nothing-sent sentence in that explanation. [Response-review design](RESPONSE_REVIEW.md).

Describe the work as an AI-assisted development experiment with inspectable failures. Personal mastery is demonstrated when you can trace a rejection to its source, predict a new failure case, and explain or implement a small change yourself; it is not established by the number of tests or iterations in the repository.

## Optional audience interaction

For an AI-tool discussion, compare the two callback handoff recordings. The model supplies the same issue ID as triage prose in both. The earlier server accepts it; the newer server rejects it with a useful error while the recorded-issue handoff still succeeds. Explain the narrow exact-match rule and then identify what the newer answer still omits: evidence citations, the proposed owner and the specific hypothesis. This demonstrates a failure-to-control development sequence without claiming that the whole answer became reliable.

Open **Compare the two callback handoff attempts** in the AI trace section. Ask which observations support the input check and which would prevent approving the final answer. Point out that the tool descriptions changed and the later explanation lost a citation. Use the two buttons to inspect the underlying recordings instead of presenting the comparison as a benchmark score.

Open [Practice](https://yuchi-wang02.github.io/csm-copilot/#practice) and invite the interviewer to choose a next action for the Android update. Explain the distinction between a failed check and an unknown check before showing the guidance. For an AI-focused discussion, use the third decision and identify the remaining omissions in the model explanation. This is a short conversation aid with published answers, not a quiz score to present as professional qualification.

## Explain what changes after a fresh test

Open the [passing-checks comparison](https://yuchi-wang02.github.io/csm-copilot/?case=lantern_android&view=evidence&lang=en&update=2#customer-update). Compare it with the original snapshot and the settings-only update. Explain which record supports each changed check, why the previous report remains recorded, and why the next draft asks whether the issue still occurs. The branch is synthetic and its proposed message is unsent. Use this as an exercise; do not describe it as a customer result or completed personal practice without doing the explanation yourself.

For the learning trail, open [the present-tense repair](https://yuchi-wang02.github.io/csm-copilot/?probe=not_failing#triage-review). Inspect the original callback recommendation and the current clarification route. The [fifth practice decision](https://yuchi-wang02.github.io/csm-copilot/?practice=question_triage#practice) uses the historical tool output, clearly labeled. Explain the seven failed-before regression checks and why a bounded fix does not establish general negation understanding or independent accuracy.

For a performance follow-up, compare the [full-history and reduced-history final requests](LOCAL_MODEL.md#reduced-final-context-lower-recorded-latency-same-field-failure). Show what was omitted, reconstruct the original history, and discuss the two recorded generation times alongside the unchanged citation rejection. Explain why a faster observed response is not evidence of a more reliable answer or a general production speedup.
