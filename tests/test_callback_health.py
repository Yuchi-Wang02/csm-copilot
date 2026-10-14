"""Bounded present-tense denial probes; expectations were authored during development."""

import json
from pathlib import Path

import pytest

from csm_copilot.engine import Copilot
from csm_copilot.models import Dataset

BEFORE = json.loads(
    (Path(__file__).resolve().parents[1] / "evidence/callback-health-before.json").read_text(
        encoding="utf-8"
    )
)


@pytest.mark.parametrize("case", BEFORE["cases"], ids=lambda c: c["id"])
def test_present_denial_preserves_questions_qualifiers_and_separate_symptoms(case):
    result = Copilot().triage_issue(case["text"])
    categories = [c["category"] for c in result["candidates"]]
    if case["kind"] == "known_limit":
        assert result == case["result"]
        assert categories != case["expected"]
    else:
        assert categories == case["expected"]
    if case["kind"] == "repair":
        assert categories != [c["category"] for c in case["result"]["candidates"]]
        assert any("callback" in n and "excluded" in n for n in result["notes"])
    assert result["root_cause"] == "unconfirmed"
    assert result["route"] == ("clarify_scope" if categories == ["unknown"] else "collect_evidence")


@pytest.mark.parametrize("complete", [False, True])
def test_callback_health_denial_leaves_invoice_request_with_csm(complete):
    data = Copilot().data.model_dump(mode="json")
    issue = next(i for i in data["issues"] if i["id"] == "issue_callback")
    issue["summary"] = BEFORE["cases"][0]["text"]
    next(e for e in data["evidence"] if e["id"] == issue["evidence_id"])["text"] = issue["summary"]
    if complete:
        issue["details"] = dict.fromkeys(
            ["sdk_version", "region", "time_window", "reproduction_steps", "redacted_logs"],
            "Synthetic detail",
        )
    engine = Copilot(Dataset.model_validate(data))
    before = engine.data.model_dump(mode="json")
    ticket = engine.draft_ticket(issue["id"])
    assert ticket["handoff_state"] == "needs_scope"
    assert ticket["suggested_owner"] == "CSM to clarify issue scope (project policy)"
    assert bool(ticket["missing_fields"]) is not complete
    assert ticket["sent"] is False
    assert ticket["root_cause"] == "unconfirmed"
    assert engine.data.model_dump(mode="json") == before
