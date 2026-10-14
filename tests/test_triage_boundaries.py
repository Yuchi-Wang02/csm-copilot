"""Bounded lexical repair, with the original semantic failures left visible."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from csm_copilot.engine import Copilot
from csm_copilot.models import Dataset

ROOT = Path(__file__).resolve().parents[1]
CASE_FILE = ROOT / "evaluation/triage_boundaries.json"
CASES = json.loads(CASE_FILE.read_text(encoding="utf-8"))
BEFORE = json.loads((ROOT / "evidence/triage-boundary-before.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_phrase_boundaries_remove_collisions_without_claiming_semantic_understanding(case):
    result = Copilot().triage_issue(case["text"])
    predicted = [item["category"] for item in result["candidates"]]
    previous = next(row["result"] for row in BEFORE["cases"] if row["id"] == case["id"])
    if case["kind"] == "known_limit":
        comparable = deepcopy(result)
        # v0.11.1 changes unknown-scope questions, not these historical category errors.
        if predicted == ["unknown"]:
            comparable["candidates"][0]["questions"] = previous["candidates"][0]["questions"]
        assert comparable == previous
        assert predicted != case["expected"]
    else:
        assert predicted == case["expected"]
    if case["kind"] == "substring_collision":
        assert previous["candidates"][0]["category"] == "no_offers"
        assert result["route"] == "clarify_scope"
        assert result["notes"] == []
    assert result["root_cause"] == "unconfirmed"


def test_before_recording_carries_the_unchanged_inputs_and_revision():
    assert (
        BEFORE["inputs_sha256"]
        == hashlib.sha256(CASE_FILE.read_text(encoding="utf-8").encode()).hexdigest()
    )
    assert BEFORE["commit"] == "a3ddd2997b014830b5da5ef7fbedae0977735a05"
    assert [(c["id"], c["text"]) for c in BEFORE["cases"]] == [(c["id"], c["text"]) for c in CASES]


@pytest.mark.parametrize("complete_fields", [False, True])
def test_invoice_collision_does_not_choose_a_technical_owner_even_with_complete_fields(
    complete_fields,
):
    data = Copilot().data.model_dump(mode="json")
    issue = next(i for i in data["issues"] if i["id"] == "issue_blank")
    issue["summary"] = "Please send the blanket invoice for our annual plan."
    source = next(e for e in data["evidence"] if e["id"] == issue["evidence_id"])
    source.update(text=issue["summary"], language="en")
    if complete_fields:
        issue["details"] = {key: "Synthetic supplied detail" for key in issue["details"]}
    result = Copilot(Dataset.model_validate(data)).draft_ticket("issue_blank")
    assert result["handoff_state"] == "needs_scope"
    assert result["suggested_owner"] == "CSM to clarify issue scope (project policy)"
    assert result["sent"] is False
