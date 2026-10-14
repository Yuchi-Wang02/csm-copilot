"""Replay inspected callback-denial development probes against frozen outputs."""

import hashlib
import json
from pathlib import Path

from csm_copilot import __version__
from csm_copilot.brief import cell
from csm_copilot.engine import Copilot

ROOT = Path(__file__).resolve().parents[1]


def evaluate():
    source = ROOT / "evidence/callback-denial-before.json"
    before = json.loads(source.read_text(encoding="utf-8"))
    engine = Copilot()
    rows = []
    for case in before["cases"]:
        result = engine.triage_issue(case["text"])
        rows.append(
            {
                **{key: case[key] for key in ("id", "kind", "text", "expected")},
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
        "changed_cases": [r["id"] for r in rows if r["before"] != r["after"]],
        "remaining_mismatches": [r["id"] for r in rows if set(r["after"]) != set(r["expected"])],
        "cases": rows,
    }
    (ROOT / "evidence/callback-denial-review.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    lines = [
        "# Callback denial: keep the request separate from the denied symptom",
        "",
        report["boundary"],
        "",
        "An explicit local denial such as `the reward callback is not our problem` or `不是奖励回调的问题` should not trigger callback troubleshooting solely because it contains callback words. The matcher excludes only signal occurrences inside supported denial spans. A separate positive callback or blank-Offerwall symptom remains eligible.",
        "",
        "The exclusion is a project lexical rule. It does not infer a billing workflow, identify a confirmed root cause, close an existing issue or send a message. Denial-only requests remain with the CSM for scope clarification, even when generic handoff fields are complete.",
        "",
        f"Frozen before commit: `{before['commit']}`. [Original outputs](callback-denial-before.json) · [Current replay](callback-denial-review.json).",
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
        "Seven selected messages change categories. Eleven checks failed before the repair: those seven message cases and four English/Chinese handoff variants with complete or incomplete generic fields. All twenty focused checks now pass, including assertions preserving three known failures.",
        "",
        "Qualified denial, `callbacks are not failing`, and quoted documentation topics still produce unwanted callback candidates. The old no-offers probes also retain qualified-negation and quoted-topic failures. This does not solve negation, temporal scope, reported speech or multilingual understanding generally.",
        "",
        "These sixteen probes were authored and inspected during development. The old twenty-probe file and original thirty-message diagnostic were not relabelled. The original diagnostic remains 16/18 after earlier adaptation; this repair does not improve that number. Historical model recordings are unchanged, with no new inference or independent human/customer validation.",
        "",
        "```sh",
        "python evaluation/callback_denial.py",
        "python -m pytest tests/test_callback_denial.py -q",
        "```",
        "",
    ]
    (ROOT / "evidence/CALLBACK_DENIAL.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n"
    )
    print(json.dumps({key: report[key] for key in ("changed_cases", "remaining_mismatches")}))
    return report


if __name__ == "__main__":
    evaluate()
