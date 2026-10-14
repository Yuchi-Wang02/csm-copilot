/* Browser and Node share the same reflection state and export rules. */
(function (root) {
  "use strict";
  function buildCases(data, modelRuns) {
    const android = data.workflow.counterfactual.after;
    const ios = data.workflow.packets
      .flatMap((p) => p.integrations)
      .find((i) => i.readiness.integration_id === "lantern_ios");
    const run = modelRuns.runs.find((r) => r.id === "qwen4-constrained");
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
        source: "#model-runs",
        sourceLabel: "Inspect the actual model attempts",
        explanation:
          "Valid structure, agreement with recorded tools, and a faithful explanation are different properties. No general model-quality score follows from this example.",
        prompt:
          "Identify two missing elements in the explanation. Explain why correction feedback changes how you would describe this result in an interview.",
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
  function line(value) {
    // Quote every user-authored line so it cannot become report structure or active HTML.
    return String(value || "[No note entered]")
      .replace(/\r\n?/g, "\n")
      .split("\n")
      .map(
        (s) =>
          "> " +
          s
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/([\\`*_{}\[\]()#+.!|~-])/g, "\\$1"),
      )
      .join("\n");
  }
  function exportReflection(cases, session, asOf) {
    const lines = [
      "# CSM Copilot — practice reflection",
      "",
      `Synthetic evidence snapshot: ${asOf}.`,
      "",
      "Self-directed practice, not an assessment or verified personal mastery. Option comparisons use this project's published policy. Written reasoning is not graded. Guidance is available in the public source; this is not a blinded test.",
      "",
    ];
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
      }
      lines.push(
        "Evidence available for this decision:",
        ...c.evidence.map(
          (e) =>
            `- ${e.label}: ${e.value.replace(/\r?\n/g, " ")} [${e.sources.join(", ") || "no applicable record"}]`,
        ),
        "",
        `Explore: https://yuchi-wang02.github.io/csm-copilot/${c.source}`,
        "",
      );
    });
    return lines.join("\n");
  }
  const api = { buildCases, createSession, reveal, exportReflection };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.CSM_PRACTICE = api;
})(typeof window !== "undefined" ? window : this);
