"""Replay the frozen present-tense callback-health development cases."""

import hashlib
import json
from pathlib import Path

from csm_copilot import __version__
from csm_copilot.engine import Copilot

ROOT = Path(__file__).resolve().parents[1]


def evaluate():
    source = ROOT / "evidence/callback-health-before.json"
    before = json.loads(source.read_text(encoding="utf-8"))
    engine = Copilot()
    rows = []
    for case in before["cases"]:
        result = engine.triage_issue(case["text"])
        rows.append(
            {
                **case,
                "before": [c["category"] for c in case["result"]["candidates"]],
                "after": [c["category"] for c in result["candidates"]],
                "after_result": result,
            }
        )
    report = {
        "project_version": __version__,
        "before_commit": before["commit"],
        "before_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "boundary": before["boundary"],
        "changed_cases": [c["id"] for c in rows if c["before"] != c["after"]],
        "remaining_mismatches": [c["id"] for c in rows if c["after"] != c["expected"]],
        "cases": rows,
    }
    (ROOT / "evidence/callback-health-review.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


if __name__ == "__main__":
    result = evaluate()
    print(json.dumps({key: result[key] for key in ("changed_cases", "remaining_mismatches")}))
