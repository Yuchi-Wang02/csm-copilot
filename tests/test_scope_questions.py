"""Unknown intent should not imply a device failure or an affected platform."""

import json
from pathlib import Path

import pytest

from csm_copilot.engine import Copilot


@pytest.mark.parametrize(
    "message",
    [
        "Please send the blanket invoice for our annual plan.",
        "想了解订阅续费的下一步安排。",
        "Can we discuss our next steps?",
    ],
)
def test_unknown_requests_get_context_and_outcome_questions_without_technical_assumptions(message):
    result = Copilot().triage_issue(message)
    assert result["route"] == "clarify_scope"
    candidate = result["candidates"][0]
    assert candidate["category"] == "unknown"
    assert candidate["checks"] == [] and candidate["source_url"] is None
    assert candidate["questions"] == [
        "Which account or product does this request concern?",
        "What specific information or outcome do you need, and which relevant details should we review?",
    ]
    assert result["root_cause"] == "unconfirmed"


def test_recognized_offerwall_questions_stay_identical_to_the_previous_recording():
    path = Path(__file__).resolve().parents[1] / "evidence/model-runs/qwen4-triage-scope.json"
    trace = json.loads(path.read_text(encoding="utf-8"))
    call = trace["steps"][0]["tool_calls"][1]
    assert Copilot().triage_issue(**call["action"]["arguments"]) == call["tool_result"]
