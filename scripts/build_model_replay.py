"""Package immutable local model traces for inspection; never rerun inference in CI."""

import hashlib
import json
from pathlib import Path

from csm_copilot.brief import text
from csm_copilot.engine import validate_draft
from csm_copilot.host_protocol import trace_coverage
from csm_copilot.response_review import review_final

ROOT = Path(__file__).resolve().parents[1]


def compare_batch_claims(trace, findings):
    """Pair two authored review claims with fields from this historical trace only."""
    specs = (
        ("iOS's full compliance", "lantern_ios", None),
        ("Android's missing evidence", "lantern_android", "device_verified"),
    )
    comparisons = []
    for claim, integration_id, check_id in specs:
        reviews = [finding for finding in findings if finding["claim"] == claim]
        if not isinstance(trace["final"], str) or claim not in trace["final"] or len(reviews) != 1:
            raise ValueError("Claim comparison requires an exact final-response excerpt and review")
        calls = [
            (step_index, call_index, call)
            for step_index, step in enumerate(trace["steps"])
            for call_index, call in enumerate(step.get("tool_calls", []))
            if call["action"]["tool"] == "check_readiness"
            and call["action"]["arguments"].get("integration_id") == integration_id
        ]
        if len(calls) != 1:
            raise ValueError("Claim comparison requires one scoped recorded readiness call")
        step_index, call_index, call = calls[0]
        result = call["tool_result"]
        if call["tool_error"] or result.get("integration_id") != integration_id:
            raise ValueError("Claim comparison requires a successful result in the requested scope")
        path = f"steps[{step_index}].tool_calls[{call_index}].tool_result"
        fields = [
            {"label": "Decision", "path": f"{path}.decision", "value": result["decision"]},
            {"label": "Scope boundary", "path": f"{path}.boundary", "value": result["boundary"]},
        ]
        if check_id:
            checks = [(i, c) for i, c in enumerate(result["checks"]) if c["id"] == check_id]
            if len(checks) != 1:
                raise ValueError("Claim comparison requires one recorded device check")
            check_index, check = checks[0]
            fields = [
                {
                    "label": check["label"],
                    "path": f"{path}.checks[{check_index}].status",
                    "value": check["status"],
                },
                {
                    "label": "Cited evidence",
                    "path": f"{path}.checks[{check_index}].evidence_ids",
                    "value": check["evidence_ids"],
                },
            ]
        comparisons.append(
            {
                "claim": claim,
                "assessment": reviews[0]["assessment"],
                "source_label": f"Turn {trace['steps'][step_index]['number']} · call {call_index + 1} · {integration_id}",
                "fields": fields,
            }
        )
    return comparisons


def compare_morning_claims(trace, findings):
    """Pair an incorrect distinction and a correct intake list with their recorded fields."""
    specs = (
        (
            "missing currency approval and device verification",
            "check_readiness",
            "integration_id",
            "lantern_android",
        ),
        ("SDK version, time window, and redacted logs", "draft_ticket", "issue_id", "issue_blank"),
    )
    rows = []
    for claim, tool, argument, identifier in specs:
        reviews = [finding for finding in findings if finding["claim"] == claim]
        if not isinstance(trace["final"], str) or claim not in trace["final"] or len(reviews) != 1:
            raise ValueError("Morning comparison requires an exact excerpt and one authored review")
        calls = [
            (s, c, call)
            for s, step in enumerate(trace["steps"])
            for c, call in enumerate(step.get("tool_calls", []))
            if call["action"]["tool"] == tool
            and call["action"]["arguments"].get(argument) == identifier
        ]
        if len(calls) != 1:
            raise ValueError("Morning comparison requires one scoped recorded call")
        s, c, call = calls[0]
        result = call["tool_result"]
        expected_scope = (
            result.get("integration_id") if tool == "check_readiness" else result.get("draft_id")
        )
        if call["tool_error"] or expected_scope != (
            identifier if tool == "check_readiness" else "ticket-" + identifier
        ):
            raise ValueError(
                "Morning comparison requires a successful result in the requested scope"
            )
        prefix = f"steps[{s}].tool_calls[{c}].tool_result"
        fields = []
        if tool == "check_readiness":
            for check_id in ("currency_approved", "device_verified"):
                checks = [
                    (i, check)
                    for i, check in enumerate(result["checks"])
                    if check["id"] == check_id
                ]
                if len(checks) != 1:
                    raise ValueError("Morning comparison requires one recorded check per ID")
                index, check = checks[0]
                fields += [
                    {
                        "label": check_id + " status",
                        "path": f"{prefix}.checks[{index}].status",
                        "value": check["status"],
                    },
                    {
                        "label": check_id + " evidence",
                        "path": f"{prefix}.checks[{index}].evidence_ids",
                        "value": check["evidence_ids"],
                    },
                ]
        else:
            fields = [
                {"label": key, "path": f"{prefix}.{key}", "value": result[key]}
                for key in ("missing_fields", "handoff_state", "root_cause", "sent")
            ]
        rows.append(
            {
                "claim": claim,
                "assessment": reviews[0]["assessment"],
                "source_label": f"Turn {trace['steps'][s]['number']} · call {c + 1} · {identifier}",
                "fields": fields,
            }
        )
    return rows


def compare_handoffs(runs):
    """Describe two existing traces; do not infer an accuracy gain from their differences."""
    ids = ("qwen4-callback-handoff", "qwen4-callback-input-guard")
    indexed = {run["id"]: run for run in runs}
    if any(identifier not in indexed for identifier in ids):
        raise ValueError("Both callback handoff recordings are required for comparison")
    pair = [indexed[identifier] for identifier in ids]
    before, after = [run["trace"] for run in pair]
    sampling = (
        "seed",
        "temperature",
        "top_p",
        "top_k",
        "max_new_tokens",
        "do_sample",
        "enable_thinking",
    )
    controls = {
        "Task text": before["task"] == after["task"],
        "Model and revision": (before["model_id"], before["revision"])
        == (after["model_id"], after["revision"]),
        "Recorded sampling settings": all(
            before["runtime"][key] == after["runtime"][key] for key in sampling
        ),
        "Initial action batch": before["steps"][0]["actions"] == after["steps"][0]["actions"],
        "System message including tool descriptions": before["initial_messages"][0]
        == after["initial_messages"][0],
    }
    attempts = []
    for run in pair:
        trace = run["trace"]
        calls = [call for step in trace["steps"] for call in step.get("tool_calls", [])]
        triage = [call for call in calls if call["action"]["tool"] == "triage_issue"]
        if len(triage) != 1:
            raise ValueError("This comparison requires one triage call in each recording")
        attempts.append(
            {
                "id": run["id"],
                "label": run["label"],
                "required_actions": f"{trace['coverage']['observed']} / {trace['coverage']['required']}",
                "attempted_calls": len(calls),
                "tool_errors": sum(bool(call["tool_error"]) for call in calls),
                "triage_input": triage[0]["action"]["arguments"]["issue_text"],
                "triage_result": "Rejected" if triage[0]["tool_error"] else "Accepted",
            }
        )
    return {"controls": controls, "attempts": attempts}


def build():
    directory = ROOT / "evidence/model-runs"
    review = json.loads((directory / "review.json").read_text(encoding="utf-8"))
    runs = []
    lines = ["# Recorded local model runs", "", review["review_method"], "", review["boundary"], ""]
    for entry in review["runs"]:
        raw = (directory / f"{entry['id']}.json").read_text(encoding="utf-8").replace("\r\n", "\n")
        trace = json.loads(raw)
        coverage = trace_coverage(trace)
        assert coverage == trace["coverage"], entry["id"]
        display_final = (
            trace["final"].get("explanation", "")
            if isinstance(trace["final"], dict)
            else trace["final"]
        )
        lint = validate_draft(display_final) if display_final else None
        if "response_review" in trace:
            assert review_final(trace["final"], trace) == trace["response_review"]
        runs.append(
            {
                **entry,
                "trace": trace,
                "sha256": hashlib.sha256(raw.encode()).hexdigest(),
                "promise_lint": lint,
                "display_final": display_final,
                "claim_comparisons": compare_batch_claims(trace, entry["findings"])
                if entry["id"] == "qwen4-batch"
                else compare_morning_claims(trace, entry["findings"])
                if entry["id"] == "qwen4-morning-long-budget"
                else [],
            }
        )
        lines += [
            f"## {text(entry['label'])}",
            "",
            f"**Review verdict:** {text(entry['verdict'])}.",
            entry["summary"],
            "",
            f"**Task:** {text(trace['task'])}",
            "",
            f"Observed requested tool actions: {coverage['observed']}/{coverage['required']}. Final response present: {coverage['final_response_present']}.",
            f"[Complete trace](model-runs/{entry['id']}.json). Model revision: `{trace['revision']}`.",
            "",
        ]
        if entry.get("host_observation"):
            lines += [f"[Separate host terminal observation]({entry['host_observation']}).", ""]
        for finding in entry["findings"]:
            lines += [
                f"- **{text(finding['kind'])}: {text(finding['claim'])}.** {text(finding['assessment'])}"
            ]
        if "response_review" in trace:
            field_review = trace["response_review"]
            lines += [
                "",
                f"Structured review: **{field_review['status']}**. Free explanation: **not semantically verified**.",
                "",
            ]
            if field_review["checked_summary"]:
                lines += ["### System-rendered summary from checked tool fields", ""]
                lines += [
                    "> " + text(line) for line in field_review["checked_summary"].splitlines()
                ]
        if display_final:
            lines += [
                "",
                "### Unedited model response — needs review",
                "",
                "> " + text(display_final),
                "",
                f"Narrow promise lint flags: {lint['flags']}. No flags does not establish fidelity.",
                "",
            ]
    payload = {
        "runs": runs,
        "review_method": review["review_method"],
        "boundary": review["boundary"],
        "handoff_comparison": {
            **compare_handoffs(runs),
            "review_rows": review["handoff_comparison"]["review_rows"],
            "boundary": review["handoff_comparison"]["boundary"],
        },
    }
    comparison = payload["handoff_comparison"]
    earlier, newer = comparison["attempts"]
    lines += ["## Compare the callback handoff attempts", "", comparison["boundary"], ""]
    lines += [
        f"- {label}: {'same' if same else 'different'}."
        for label, same in comparison["controls"].items()
    ]
    lines += ["", "| Recorded observation | Earlier run | With identifier check |", "|---|---|---|"]
    for label, key in [
        ("Requested actions observed", "required_actions"),
        ("Total attempted calls", "attempted_calls"),
        ("Tool errors", "tool_errors"),
        ("Triage input", "triage_input"),
        ("Triage result", "triage_result"),
    ]:
        lines.append(f"| {label} | {text(str(earlier[key]))} | {text(str(newer[key]))} |")
    lines += [
        "",
        "### Source comparison — AI-assisted",
        "",
        "| Review point | Earlier answer | Newer answer |",
        "|---|---|---|",
    ]
    for row in comparison["review_rows"]:
        lines.append(f"| {text(row['label'])} | {text(row['before'])} | {text(row['after'])} |")
    lines += [
        "",
        f"[Earlier trace](model-runs/{earlier['id']}.json) · [Newer trace](model-runs/{newer['id']}.json)",
        "",
    ]
    (ROOT / "demo/model-runs.js").write_text(
        "window.CSM_MODEL_RUNS = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
        newline="\n",
    )
    (ROOT / "evidence/MODEL_RUNS.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"Packaged {len(runs)} recorded model runs; no inference performed.")
    return payload


if __name__ == "__main__":
    build()
