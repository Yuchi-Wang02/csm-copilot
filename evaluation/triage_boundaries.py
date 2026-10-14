"""Compare a bounded lexical repair with recorded pre-change engine outputs."""

import hashlib
import json
from pathlib import Path

from csm_copilot import __version__
from csm_copilot.brief import cell
from csm_copilot.engine import Copilot

ROOT = Path(__file__).resolve().parents[1]


def evaluate():
    case_file = ROOT / "evaluation/triage_boundaries.json"
    cases = json.loads(case_file.read_text(encoding="utf-8"))
    before = json.loads((ROOT / "evidence/triage-boundary-before.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256(case_file.read_text(encoding="utf-8").encode()).hexdigest()
    assert digest == before["inputs_sha256"], "Do not silently change recorded diagnostic inputs"
    assert [(c["id"], c["text"]) for c in cases] == [(c["id"], c["text"]) for c in before["cases"]]
    engine = Copilot()
    rows = []
    for case, recorded in zip(cases, before["cases"], strict=True):
        result = engine.triage_issue(case["text"])
        previous = [c["category"] for c in recorded["result"]["candidates"]]
        current = [c["category"] for c in result["candidates"]]
        rows.append(
            {
                **case,
                "before_categories": previous,
                "after_categories": current,
                "before_correct": set(previous) == set(case["expected"]),
                "after_correct": set(current) == set(case["expected"]),
                "after_result": result,
            }
        )
    report = {
        "project_version": __version__,
        "before_commit": before["commit"],
        "inputs_sha256": digest,
        "boundary": "AI-assisted development probes authored for this repair, including two known failures reused from the original diagnostic set. Not an independent test or a general accuracy estimate.",
        "model_inference": False,
        "changed_cases": [r["id"] for r in rows if r["before_categories"] != r["after_categories"]],
        "remaining_mismatches": [r["id"] for r in rows if not r["after_correct"]],
        "cases": rows,
    }
    (ROOT / "evidence/triage-boundary-review.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    lines = [
        "# Triage phrase-boundary repair",
        "",
        report["boundary"],
        "",
        "## What changed",
        "",
        "The earlier lexical pattern matched `blank` inside `blanket`, `no offers` inside `casino offers`, and `no ads` inside `no adservers`. An unrelated invoice request could therefore receive Offerwall checks and a proposed technical handoff.",
        "",
        "The English no-offers phrases now have Latin-letter boundaries. Common forms such as blanking and empty offerwalls remain supported, and Chinese characters can sit directly beside an English signal. Chinese signals and reward/callback retrieval are unchanged. This is a narrow lexical repair, not semantic classification or a general tokenizer.",
        "",
        f"[Pre-change code](https://github.com/Yuchi-Wang02/csm-copilot/blob/{before['commit']}/src/csm_copilot/engine.py) · [Recorded pre-change engine outputs](triage-boundary-before.json) · [Current outputs](triage-boundary-review.json)",
        "",
        "## Paired observations",
        "",
        "| Probe | Customer message | Expected | Before | After |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                cell(x)
                for x in (
                    row["id"],
                    row["text"],
                    ", ".join(row["expected"]),
                    ", ".join(row["before_categories"]),
                    ", ".join(row["after_categories"]),
                )
            )
            + " |"
        )
    lines += [
        "",
        f"Changed categories on {len(report['changed_cases'])} of these 12 development probes. {len(report['remaining_mismatches'])} known semantic failures remain. These counts describe this selected set only.",
        "",
        "## Workflow consequence",
        "",
        "The blanket-invoice example now returns `clarify_scope`. A ticket based on that message stays with the CSM to clarify the problem, even when generic SDK/log fields are present. It does not classify billing or choose a Finance owner; those capabilities are outside this prototype.",
        "",
        "Six regression checks failed before the repair and passed afterward: four substring collisions and two handoff variants with complete/incomplete generic fields. Six positive-message probes retain their expected categories. The two known semantic failures are intentionally still failures.",
        "",
        "## Limits and reproduction",
        "",
        "The original 30-message diagnostic inputs are unchanged. Its 14/18 family-separated result remains unchanged: negation and indirect wording still fail. The new probes were authored during this repair and are not held out. No independent human labeling, model run, customer outcome or productivity measurement was performed.",
        "A standalone term such as blank can still describe an invoice or another unrelated object. Phrase boundaries do not determine whether the sentence reports an Offerwall problem.",
        "",
        "```sh",
        "python evaluation/triage_boundaries.py",
        "python -m pytest tests/test_triage_boundaries.py -q",
        "```",
        "",
        f"Inputs SHA-256: `{digest}`",
        "",
    ]
    (ROOT / "evidence/TRIAGE_BOUNDARIES.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n"
    )
    print(
        json.dumps(
            {
                "changed_cases": report["changed_cases"],
                "remaining_mismatches": report["remaining_mismatches"],
            }
        )
    )
    return report


if __name__ == "__main__":
    evaluate()
