"""Replay inspected development probes; preserve original outputs and remaining failures."""

import hashlib
import json
from pathlib import Path

from csm_copilot import __version__
from csm_copilot.brief import cell
from csm_copilot.engine import Copilot

ROOT = Path(__file__).resolve().parents[1]


def evaluate():
    inputs = ROOT / "evaluation/negation_cases.json"
    cases = json.loads(inputs.read_text(encoding="utf-8"))
    before = json.loads((ROOT / "evidence/negation-before.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256(inputs.read_text(encoding="utf-8").encode()).hexdigest()
    assert digest == before["inputs_sha256"]
    engine = Copilot()
    rows = []
    for case, old in zip(cases, before["cases"], strict=True):
        assert case == {key: old[key] for key in case}
        result = engine.triage_issue(case["text"])
        previous = [c["category"] for c in old["result"]["candidates"]]
        current = [c["category"] for c in result["candidates"]]
        rows.append({**case, "before": previous, "after": current, "after_result": result})
    report = {
        "project_version": __version__,
        "before_commit": before["commit"],
        "inputs_sha256": digest,
        "boundary": "Twenty AI-assisted developer-authored probes inspected while building this rule. Not held out, independently labelled or a general accuracy estimate. No model inference.",
        "changed_cases": [r["id"] for r in rows if r["before"] != r["after"]],
        "remaining_mismatches": [r["id"] for r in rows if set(r["after"]) != set(r["expected"])],
        "cases": rows,
    }
    (ROOT / "evidence/negation-review.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    lines = [
        "# Explicit denial in triage: a bounded repair",
        "",
        report["boundary"],
        "",
        "## Decision and implementation",
        "",
        "A message explicitly denying a no-offers problem should not become a technical handoff solely because the denied phrase occurs in the text. The matcher now excludes signal occurrences contained in supported local denial patterns. It still evaluates other occurrences and callback signals separately. It does not discard an entire sentence or message after seeing `not`.",
        "",
        "Supported forms include `no offers is not our problem`, `isn't blank`, `不是没有广告的问题`, and `页面并不空白`. Another platform's positive symptom survives, as do `not only blank` and `not our only problem`. The result notes when a denial was excluded. Root cause remains unconfirmed.",
        "",
        "## Recorded before and after",
        "",
        f"Original code commit: `{before['commit']}`. [Frozen outputs and original diagnostic](negation-before.json) · [Current replay](negation-review.json).",
        "",
        "| Probe | Message | Expected | Before | Current |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                cell(value)
                for value in (
                    row["id"],
                    row["text"],
                    ", ".join(row["expected"]),
                    ", ".join(row["before"]),
                    ", ".join(row["after"]),
                )
            )
            + " |"
        )
    lines += [
        "",
        f"Categories change on {len(report['changed_cases'])} selected probes. {len(report['remaining_mismatches'])} selected counterexamples still fail. Twelve regression checks failed before the repair: ten message cases and two handoff variants. The 24-check regression suite retains the frozen inputs and separate positive signals. The originally recorded callback-denial failure is now repaired by the separately documented callback rule.",
        "",
        "## What the score cannot establish",
        "",
        "The original 30-message diagnostic is unchanged, but its negation cases informed this rule. Its earlier 14/18 family-separated result is preserved in the frozen record. The current 16/18 is a replay after adaptation on inspected cases, not an independent improvement estimate. The remaining English and Chinese indirect-inventory cases still fail. No model run or human customer review was added by this change.",
        "",
        "Qualified negation (`isn't exactly blank`) and quoted search topics remain counterexamples here. The [callback-denial review](CALLBACK_DENIAL.md) preserves the original callback failure, its bounded repair and three remaining callback counterexamples. Nested denial, reported speech, temporal scope and multilingual nuance require semantic review; this pattern list does not solve negation generally. A standalone `blank` may also describe something unrelated to Offerwall.",
        "",
        "## Workflow consequence",
        "",
        "A denied no-offers message with no other recognized symptom remains `clarify_scope`; its handoff stays `needs_scope` with the CSM even if generic logs/SDK fields are complete. A separate callback symptom remains eligible for evidence collection. No billing owner is invented and no message or ticket is sent.",
        "",
        "```sh",
        "python evaluation/negation.py",
        "python -m pytest tests/test_negation.py -q",
        "```",
        "",
        f"Inputs SHA-256: `{digest}`",
        "",
    ]
    (ROOT / "evidence/NEGATION_REVIEW.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n"
    )
    print(json.dumps({key: report[key] for key in ("changed_cases", "remaining_mismatches")}))
    return report


if __name__ == "__main__":
    evaluate()
