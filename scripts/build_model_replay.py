"""Package immutable local model traces for inspection; never rerun inference in CI."""

import hashlib
import json
from pathlib import Path

from csm_copilot.brief import text
from csm_copilot.engine import validate_draft
from csm_copilot.host_protocol import trace_coverage

ROOT = Path(__file__).resolve().parents[1]


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
        lint = validate_draft(trace["final"]) if trace["final"] else None
        runs.append(
            {
                **entry,
                "trace": trace,
                "sha256": hashlib.sha256(raw.encode()).hexdigest(),
                "promise_lint": lint,
            }
        )
        lines += [
            f"## {text(entry['label'])}",
            "",
            f"**Review verdict:** {text(entry['verdict'])}.",
            entry["summary"],
            "",
            f"Observed requested tool actions: {coverage['observed']}/{coverage['required']}. Final response present: {coverage['final_response_present']}.",
            f"[Complete trace](model-runs/{entry['id']}.json). Model revision: `{trace['revision']}`.",
            "",
        ]
        for finding in entry["findings"]:
            lines += [
                f"- **{text(finding['kind'])}: {text(finding['claim'])}.** {text(finding['assessment'])}"
            ]
        if trace["final"]:
            lines += [
                "",
                "### Unedited model response — needs review",
                "",
                "> " + text(trace["final"]),
                "",
                f"Narrow promise lint flags: {lint['flags']}. No flags does not establish fidelity.",
                "",
            ]
    payload = {
        "runs": runs,
        "review_method": review["review_method"],
        "boundary": review["boundary"],
    }
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
