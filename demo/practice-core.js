/* Browser and Node share the same reflection state and export rules. */
(function (root) {
  "use strict";
  function buildCases(data, modelRuns) {
    const android = data.workflow.counterfactual.after;
    const ios = data.workflow.packets
      .flatMap((p) => p.integrations)
      .find((i) => i.readiness.integration_id === "lantern_ios");
    const run = modelRuns.runs.find((r) => r.id === "qwen4-constrained");
    const harbor = data.workflow.packets.find((p) => p.context.account.id === "acc_006");
    const callback = harbor.tickets.find((t) => t.draft_id === "ticket-issue_callback");
    const report = harbor.context.evidence.find((e) => e.id === "msg_issue_callback");
    const denial = data.callback_denial.cases.find((c) => c.id === "not_failing");
    return [
      {
        id: "android_update",
        title: "Two settings confirmed. What comes next?",
        situation:
          "Lantern Games confirms Android currency approval and that Test Only is off. No new non-test-device result has arrived. Choose the most defensible next action under this project's policy.",
        evidence: android.checks.map((c) => ({
          label: c.label,
          value: c.status,
          sources: c.evidence_ids,
        })),
        options: [
          {
            id: "approve",
            text: "Confirm Friday's launch now that both settings are fixed.",
            feedback:
              "Those confirmations do not resolve the recorded device failure or supply callback evidence. The checklist cannot approve a launch.",
          },
          {
            id: "retest",
            text: "Request a fresh non-test-device result and callback evidence; keep the unresolved checks visible.",
            feedback:
              "The settings now have evidence, but device_verified remains not_met and callback_verified remains unknown. A retest and missing evidence address different gaps.",
          },
          {
            id: "reuse",
            text: "Use the successful iOS checks to close the remaining Android items.",
            feedback:
              "The iOS records describe another integration. Source identity and platform scope must remain separate.",
          },
        ],
        expected: "retest",
        source:
          "?case=lantern_android&view=evidence&lang=en&update=1#customer-update",
        sourceLabel: "Inspect the case explorer and customer update",
        explanation:
          "Keep a recorded failure separate from an unknown state. Ask for new evidence without claiming the issue is resolved.",
        prompt:
          "Write the next two sentences you would send to the customer. Which source supports the failure, and which evidence is still missing?",
      },
      {
        id: "ios_followup",
        title: "The checklist is complete. What should the follow-up ask?",
        situation:
          "Lantern's iOS integration has met all six scoped checks. No issue is recorded for this integration. Choose the follow-up that fits the current evidence.",
        evidence: ios.readiness.checks.map((c) => ({
          label: c.label,
          value: c.status,
          sources: c.evidence_ids,
        })),
        options: [
          {
            id: "review",
            text: "Confirm changes since the checks and review the current launch plan.",
            feedback: ios.followup_en.next_action,
          },
          {
            id: "repeat",
            text: "Ask for all six items again as though they were missing.",
            feedback:
              "The recorded evidence already meets these scoped checks. Ask about changes and launch plans instead of treating known evidence as absent.",
          },
          {
            id: "guarantee",
            text: "Confirm full compliance and guarantee ad availability.",
            feedback:
              "This project checks six onboarding items. It does not evaluate full compliance or guarantee launch or ad availability.",
          },
        ],
        expected: "review",
        source: "?case=lantern_ios&view=followup&lang=en#workspace",
        sourceLabel: "Inspect Lantern's iOS evidence and follow-up",
        explanation:
          "A complete scoped checklist changes the follow-up from evidence collection to launch-plan review. It does not establish launch approval, full compliance or ad availability.",
        prompt:
          "Explain why the Android and iOS follow-ups differ without implying launch approval. What new information could change this next action?",
      },
      {
        id: "model_review",
        title: "The fields match. Is the model's explanation ready to send?",
        situation:
          "A local model executed all four requested tools. After two recorded corrections, its structured fields matched those results. Decide what that result lets you conclude.",
        evidence: [
          {
            label: "Structured field review",
            value: run.trace.response_review.status,
            sources: ["qwen4-constrained.json: response_review"],
          },
          {
            label: "Free-text verification",
            value: run.trace.response_review.free_text_verification,
            sources: ["qwen4-constrained.json: response_review"],
          },
          {
            label: "Correction requests",
            value: String(
              run.trace.steps.filter((s) => s.correction_feedback).length,
            ),
            sources: ["qwen4-constrained.json: steps"],
          },
          {
            label: "Unedited model explanation",
            value: run.display_final,
            sources: ["qwen4-constrained.json: final.explanation"],
          },
        ],
        options: [
          {
            id: "accuracy",
            text: "Report 100% model accuracy because all four tools ran.",
            feedback:
              "Tool coverage is not answer accuracy. This is one development task with changed settings and correction feedback supplying expected values.",
          },
          {
            id: "send",
            text: "Send the explanation because the JSON schema and field checks passed.",
            feedback:
              "Neither check evaluates all free-form claims or instruction compliance. This explanation still lacks inline source IDs and the explicit nothing-sent sentence.",
          },
          {
            id: "separate",
            text: "Use the checked fields as a review aid and examine the explanation separately.",
            feedback:
              "Field agreement is a narrower result than faithful prose. The separate system-rendered summary preserves the checked states and source IDs; customer use still requires review.",
          },
        ],
        expected: "separate",
        source: "?run=qwen4-constrained#model-runs",
        sourceLabel: "Inspect the constrained recording used in this exercise",
        explanation:
          "Valid structure, agreement with recorded tools, and a faithful explanation are different properties. No general model-quality score follows from this example.",
        prompt:
          "Identify two missing elements in the explanation. Explain why correction feedback changes how you would describe this result in an interview.",
      },
      {
        id: "callback_handoff",
        title: "The customer already gave details. What should you ask next?",
        situation:
          "Harbor reports a reward callback problem. Read the original record and existing handoff fields, then choose a focused follow-up. Nothing has been sent or submitted.",
        evidence: [
          {label: "Original issue record", value: report.text, sources: [report.id]},
          {label: "Declared source type and date", value: `${report.kind} · ${report.at}`, sources: [report.id]},
          {label: "Recorded SDK, region and time window", value: `${callback.fields.sdk_version}; ${callback.fields.region}; ${callback.fields.time_window}`, sources: [report.id]},
          {label: "Missing handoff fields", value: callback.missing_fields.join(", "), sources: [callback.draft_id]},
          {label: "Root cause", value: callback.root_cause, sources: [callback.draft_id]},
        ],
        options: [
          {
            id: "repeat_all",
            text: "Ask for currency mode, SDK version, region and time window again before proceeding.",
            feedback:
              "The report already gives self-managed currency, SDK version, Japan and the observation window. Reuse those details unless clarification or a fresh confirmation is needed; the generic questions are a review aid, not a script to send unchanged.",
          },
          {
            id: "collect_missing",
            text: "Acknowledge the supplied details; request reproduction steps and a redacted callback example with logs and endpoint method.",
            feedback:
              "The handoff lacks reproduction steps and redacted logs. A callback example and endpoint method address the existing candidate checks without treating HTTP 405 as a confirmed cause. Keep the recorded time window and ask whether the new example comes from that attempt or a later one.",
          },
          {
            id: "diagnose",
            text: "Tell the customer the endpoint method is wrong and promise that changing it will restore rewards.",
            feedback:
              "HTTP 405 makes a method mismatch worth investigating, but this record does not confirm the cause or the outcome of a change. Do not turn a candidate into a diagnosis or a resolution promise.",
          },
        ],
        expected: "collect_missing",
        source: "?case=harbor_android&view=handoff&lang=en#workspace",
        sourceLabel: "Inspect Harbor's original report and handoff questions",
        explanation:
          "Use what the customer already supplied, request the specific gaps, and preserve uncertainty about the cause. A useful handoff combines source-linked facts with focused investigation questions.",
        prompt:
          "Draft a two-sentence follow-up in your own words. Which supplied details would you acknowledge, what would you request, and how would you avoid stating a diagnosis?",
      },
      {
        id: "question_triage",
        title: "The tool suggests callbacks. What is the customer asking for?",
        situation:
          "Review this synthetic customer message alongside the tool output recorded before the present-tense denial repair. Choose the next action you would have taken before drafting a reply.",
        evidence: [
          {label: "Customer message", value: denial.text, sources: ["callback-denial-review.json: not_failing.text"]},
          {label: "Recorded tool candidate categories", value: denial.before_result.candidates.map((c) => c.category).join(", "), sources: ["not_failing.before_result.candidates"]},
          {label: "Recorded tool route", value: denial.before_result.route, sources: ["not_failing.before_result.route"]},
          {label: "Recorded tool follow-up questions", value: denial.before_result.candidates.flatMap((c) => c.questions).join(" "), sources: ["not_failing.before_result.candidates"]},
          {label: "Root cause", value: denial.before_result.root_cause, sources: ["not_failing.before_result.root_cause"]},
        ],
        options: [
          {
            id: "follow_tool",
            text: "Send the callback questions: request currency mode, HTTP status and redacted logs.",
            feedback:
              "Those questions follow the retrieved callback category but overlook the invoice request. The recorded tool output misread this denial wording. Review the customer's intent before adopting the generated next step.",
          },
          {
            id: "clarify_invoice",
            text: "Acknowledge the invoice question and ask which account, invoice or billing detail needs explanation.",
            feedback:
              "The customer asks about invoicing and denies a callback failure. Clarify that request before proposing an owner or a resolution. This demo has no billing classifier or verified Finance routing policy.",
          },
          {
            id: "certify_healthy",
            text: "Confirm that callbacks are verified healthy and promise Finance will correct the invoice today.",
            feedback:
              "A customer's denial is not a technical verification. No invoice error, Finance owner or resolution time has been established, so these claims go beyond the evidence.",
          },
        ],
        expected: "clarify_invoice",
        source: "?probe=not_failing#triage-review",
        sourceLabel: "Inspect the preserved failure and current repair",
        explanation:
          "This recorded failure was later repaired by a bounded present-tense rule; the original output remains available for review. Keep the customer's stated intent separate from a tool's retrieved category, and keep a reported absence of trouble separate from verified technical health. The comparison is project-authored guidance, not independent validation.",
        prompt:
          "Write a two-sentence reply that addresses invoicing without certifying callback health or promising a resolution. Which part of the tool output would you question, and what information would you request next?",
      },
    ];
  }
  function createSession(cases) {
    return cases.map((c) => ({
      id: c.id,
      choice: "",
      reasoning: "",
      reviewed: false,
      initial: null,
      reflection: "",
    }));
  }
  function reveal(item, decision) {
    if (item.reviewed || !decision.options.some((o) => o.id === item.choice))
      return item;
    return {
      ...item,
      reviewed: true,
      initial: { choice: item.choice, reasoning: item.reasoning },
    };
  }
  function hasWork(session) {
    return session.some((item) => item.reviewed || item.choice || item.reasoning.trim());
  }
  function literal(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/([\\`*_{}\[\]()#+.!|~-])/g, "\\$1");
  }
  function inline(value) {
    return literal(String(value).replace(/\r\n?|\n/g, " "));
  }
  function line(value) {
    // Quote every user-authored line so it cannot become report structure or active HTML.
    return String(value || "[No note entered]")
      .replace(/\r\n?/g, "\n")
      .split("\n")
      .map((s) => "> " + literal(s))
      .join("\n");
  }
  function exportReflection(cases, session, asOf, restored = false) {
    const lines = [
      "# CSM Copilot — practice reflection",
      "",
      `Synthetic evidence snapshot: ${asOf}.`,
      "",
      "Self-directed practice, not an assessment or verified personal mastery. Option comparisons use this project's published policy. Written reasoning is not graded. Guidance is available in the public source; this is not a blinded test.",
      "",
      "Unreviewed choices and notes are drafts captured without revealing guidance in this session. They remain editable in the page. This download is a readable record, not a file that can restore the browser session.",
      "",
    ];
    if (restored) lines.push(
      "This session was resumed from a user-editable local progress file. Original-response and guidance labels reflect the saved state; they do not verify authorship, timing or unaided work.", "",
    );
    cases.forEach((c, index) => {
      const item = session[index];
      lines.push(
        `## ${index + 1}. ${c.title}`,
        "",
        item.reviewed ? "Status: guidance revealed." : "Status: not reviewed.",
        "",
      );
      if (item.reviewed) {
        const chosen = c.options.find((o) => o.id === item.initial.choice);
        lines.push(
          "Original choice:",
          line(chosen.text),
          "",
          "Reasoning captured before guidance:",
          line(item.initial.reasoning),
          "",
          `Option comparison: ${item.initial.choice === c.expected ? "matches" : "differs from"} the project policy. Written reasoning remains ungraded.`,
          "",
          "Project guidance:",
          line(c.explanation),
          "",
          "Reflection written after guidance:",
          line(item.reflection),
          "",
        );
      } else if (item.choice || item.reasoning.trim()) {
        const chosen = c.options.find((o) => o.id === item.choice);
        lines.push(
          "Draft choice (not compared with guidance):",
          line(chosen ? chosen.text : "[No option selected]"),
          "",
          "Draft reasoning (guidance not revealed):",
          line(item.reasoning),
          "",
        );
      }
      lines.push(
        "Evidence available for this decision:",
        ...c.evidence.map(
          (e) =>
            `- ${inline(e.label)}: ${inline(e.value)} [${inline(e.sources.join(", ") || "no applicable record")}]`,
        ),
        "",
        `Explore: https://yuchi-wang02.github.io/csm-copilot/${c.source}`,
        "",
      );
    });
    return lines.join("\n");
  }
  const api = { buildCases, createSession, reveal, hasWork, exportReflection };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CSM_PRACTICE = api;
})(typeof window !== "undefined" ? window : this);
