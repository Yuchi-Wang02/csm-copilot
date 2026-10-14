"""Package immutable local model traces for inspection; never rerun inference in CI."""

import hashlib
import json
from pathlib import Path

from csm_copilot.brief import text
from csm_copilot.engine import validate_draft
from csm_copilot.host_protocol import trace_coverage
from csm_copilot.response_review import review_final

ROOT = Path(__file__).resolve().parents[1]


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
