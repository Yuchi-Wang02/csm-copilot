"""Inspected development cases, including counterexamples; not a benchmark."""

import json
from pathlib import Path

import pytest

from csm_copilot.engine import Copilot
from csm_copilot.models import Dataset

BEFORE = json.loads(
    (Path(__file__).resolve().parents[1] / "evidence/callback-denial-before.json").read_text(
        encoding="utf-8"
    )
)


@pytest.mark.parametrize("case", BEFORE["cases"], ids=lambda case: case["id"])
def test_callback_mentions_preserve_separate_positive_signals(case):
    result = Copilot().triage_issue(case["text"])
    categories = [c["category"] for c in result["candidates"]]
    if case["kind"] == "known_limit" and case["id"] != "not_failing":
        assert result == case["result"]
        assert categories != case["expected"]
    else:
        assert categories == case["expected"]
        assert result["route"] == (
            "clarify_scope" if categories == ["unknown"] else "collect_evidence"
        )
    if case["kind"] == "repair" or case["id"] == "not_failing":
        assert [c["category"] for c in case["result"]["candidates"]] != case["expected"]
        assert any("callback" in note and "excluded" in note for note in result["notes"])
    assert result["root_cause"] == "unconfirmed"


@pytest.mark.parametrize(
    "text",
    [
        "The reward callback is not our problem. Please explain invoicing.",
        "不是奖励回调的问题，请说明账单。",
    ],
)
@pytest.mark.parametrize("complete", [False, True])
def test_denied_callback_does_not_create_a_technical_handoff(text, complete):
    data = Copilot().data.model_dump(mode="json")
    issue = next(i for i in data["issues"] if i["id"] == "issue_callback")
    issue["summary"] = text
    next(e for e in data["evidence"] if e["id"] == issue["evidence_id"])["text"] = text
    if complete:
        issue["details"] = {
            key: "Synthetic supplied detail"
            for key in (
                "sdk_version",
                "region",
                "time_window",
                "reproduction_steps",
                "redacted_logs",
            )
        }
    engine = Copilot(Dataset.model_validate(data))
    original = engine.data.model_dump(mode="json")
    ticket = engine.draft_ticket("issue_callback")
    assert ticket["handoff_state"] == "needs_scope"
    assert ticket["suggested_owner"] == "CSM to clarify issue scope (project policy)"
    assert bool(ticket["missing_fields"]) is not complete
    assert ticket["sent"] is False
    assert engine.data.model_dump(mode="json") == original
