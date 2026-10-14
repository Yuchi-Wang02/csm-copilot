"""Developer-authored repairs and preserved counterexamples; not a held-out score."""

import hashlib
import json
from pathlib import Path

import pytest

from csm_copilot.engine import Copilot
from csm_copilot.models import Dataset

ROOT = Path(__file__).resolve().parents[1]
CASE_FILE = ROOT / "evaluation/negation_cases.json"
CASES = json.loads(CASE_FILE.read_text(encoding="utf-8"))
BEFORE = json.loads((ROOT / "evidence/negation-before.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_denied_mentions_do_not_erase_separate_positive_signals(case):
    result = Copilot().triage_issue(case["text"])
    categories = [c["category"] for c in result["candidates"]]
    # Keep frozen labels intact: callback_denial was a known limit when recorded,
    # and is now covered by the separately preserved callback-denial repair.
    if case["kind"] == "known_limit" and case["id"] != "callback_denial":
        previous = next(c["result"] for c in BEFORE["cases"] if c["id"] == case["id"])
        assert result == previous
        assert categories != case["expected"]
    else:
        assert categories == case["expected"]
        assert result["route"] == (
            "clarify_scope" if categories == ["unknown"] else "collect_evidence"
        )
    assert result["root_cause"] == "unconfirmed"


def test_frozen_inputs_and_original_diagnostic_have_not_been_relabelled():
    assert hashlib.sha256(CASE_FILE.read_bytes()).hexdigest() == BEFORE["inputs_sha256"]
    original = BEFORE["original_diagnostic"]
    assert original["metrics"]["holdout"]["correct"] == 14
    assert (
        original["cases_sha256"]
        == hashlib.sha256(
            (ROOT / "evaluation/cases.json").read_text(encoding="utf-8").encode()
        ).hexdigest()
    )


@pytest.mark.parametrize("complete_fields", [False, True])
def test_a_denied_symptom_does_not_create_a_technical_handoff(complete_fields):
    data = Copilot().data.model_dump(mode="json")
    issue = next(i for i in data["issues"] if i["id"] == "issue_blank")
    issue["summary"] = "No offers is not our problem. Please explain invoicing."
    source = next(e for e in data["evidence"] if e["id"] == issue["evidence_id"])
    source.update(text=issue["summary"], language="en")
    if complete_fields:
        issue["details"] = {key: "Synthetic supplied detail" for key in issue["details"]}
    result = Copilot(Dataset.model_validate(data)).draft_ticket("issue_blank")
    assert result["handoff_state"] == "needs_scope"
    assert result["suggested_owner"] == "CSM to clarify issue scope (project policy)"
    assert result["sent"] is False


def test_original_diagnostic_changes_only_the_two_inspected_denial_cases():
    engine = Copilot()
    changed = []
    for case in BEFORE["original_diagnostic"]["triage_cases"]:
        categories = [c["category"] for c in engine.triage_issue(case["text"])["candidates"]]
        if categories != case["predicted"]:
            changed.append(case["id"])
            assert categories == case["expected"]
    assert changed == ["negated_symptom_en", "negated_symptom_zh"]
