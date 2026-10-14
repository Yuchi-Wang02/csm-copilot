"""Integrity of published recordings, not a rerun or independent model-quality test."""

import hashlib
import json
from pathlib import Path

import pytest

from csm_copilot.engine import Copilot
from csm_copilot.host_protocol import trace_coverage
from csm_copilot.response_review import review_final

DIRECTORY = Path(__file__).resolve().parents[1] / "evidence/model-runs"


@pytest.mark.parametrize(
    "name",
    [
        "qwen06-single",
        "qwen4-single",
        "qwen4-batch",
        "qwen4-grounded",
        "qwen4-grounded-corrections",
        "qwen4-constrained",
        "qwen4-callback-handoff",
        "qwen4-callback-input-guard",
        "qwen4-triage-scope",
    ],
)
def test_recorded_prompt_and_coverage_match_trace(name):
    trace = json.loads((DIRECTORY / f"{name}.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256(
        json.dumps(trace["initial_messages"], ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()
    assert digest == trace["prompt_sha256"]
    assert trace_coverage(trace) == trace["coverage"]
    assert trace["model_inference"] is True
    assert trace["runtime"]["enable_thinking"] is False


def test_published_tool_results_match_the_underlying_fixture():
    trace = json.loads((DIRECTORY / "qwen4-batch.json").read_text(encoding="utf-8"))
    engine = Copilot()
    calls = [c for step in trace["steps"] for c in step.get("tool_calls", [])]
    assert len(calls) == 4
    methods = {"check_readiness": engine.check_readiness, "draft_followup": engine.draft_followup}
    for call in calls:
        action = call["action"]
        assert methods[action["tool"]](**action["arguments"]) == call["tool_result"]
    assert trace["final"]  # Prose is separately reviewed, not approved by this test.


def test_inbound_scope_recording_preserves_inputs_routes_and_unedited_prose():
    from csm_copilot.host_protocol import TRIAGE_SCOPE_MESSAGES

    trace = json.loads((DIRECTORY / "qwen4-triage-scope.json").read_text(encoding="utf-8"))
    assert trace["task_id"] == "triage_scope"
    assert trace["project_version"] == "0.11.0"
    assert trace["coverage"]["observed"] == trace["coverage"]["required"] == 2
    assert trace["repair_budget"] == 0
    calls = [c for s in trace["steps"] for c in s.get("tool_calls", [])]
    assert len(calls) == 2
    assert [c["action"]["arguments"]["issue_text"] for c in calls] == list(
        TRIAGE_SCOPE_MESSAGES.values()
    )
    engine = Copilot()
    for call in calls:
        assert call["action"]["tool"] == "triage_issue"
        assert call["action"]["arguments"]["integration_id"] is None
        assert not call["tool_error"]
        assert call["tool_result"] == engine.triage_issue(**call["action"]["arguments"])
    assert [c["tool_result"]["route"] for c in calls] == ["clarify_scope", "collect_evidence"]
    assert not any("correction_feedback" in s for s in trace["steps"])
    assert json.loads(trace["steps"][-1]["model_response"]["text"])["final"] == trace["final"]


def test_recorded_corrections_and_field_reviews_are_reproducible():
    trace = json.loads((DIRECTORY / "qwen4-constrained.json").read_text(encoding="utf-8"))
    corrections = [s for s in trace["steps"] if "correction_feedback" in s]
    assert len(corrections) == 2
    assert [s["repair_number"] for s in corrections] == [1, 2]
    for index, step in enumerate(trace["steps"]):
        if "response_review" in step:
            prefix = {**trace, "steps": trace["steps"][: index + 1]}
            final = step["actions"][0]["final"]
            assert review_final(final, prefix) == step["response_review"]
            assert step["model_response"]["schema_constrained"] is True
    assert trace["status"] == "structured_fields_match"
    assert review_final(trace["final"], trace) == trace["response_review"]
    assert trace["response_review"]["free_text_verification"] == "not_performed"


def test_callback_handoff_preserves_the_historical_identifier_input_error():
    trace = json.loads((DIRECTORY / "qwen4-callback-handoff.json").read_text(encoding="utf-8"))
    assert trace["task_id"] == "callback_handoff"
    assert trace["coverage"]["observed"] == trace["coverage"]["required"] == 2
    engine = Copilot()
    calls = [c for step in trace["steps"] for c in step.get("tool_calls", [])]
    assert len(calls) == 4
    for call in calls:
        action = call["action"]
        if action["tool"] == "triage_issue":
            # The v0.9 recording is immutable. v0.9.1 rejects this formerly accepted input.
            assert action["arguments"]["issue_text"] == "issue_callback"
            assert call["tool_error"] is False
            assert call["tool_result"]["candidates"][0]["category"] == "reward_callback"
            with pytest.raises(ValueError, match="customer message, not a recorded issue ID"):
                engine.triage_issue(**action["arguments"])
            continue
        assert getattr(engine, action["tool"])(**action["arguments"]) == call["tool_result"]
    assert not any("correction_feedback" in step for step in trace["steps"])


def test_identifier_check_recording_preserves_the_tool_error_and_successful_handoff():
    trace = json.loads((DIRECTORY / "qwen4-callback-input-guard.json").read_text(encoding="utf-8"))
    previous = json.loads((DIRECTORY / "qwen4-callback-handoff.json").read_text(encoding="utf-8"))
    assert trace["project_version"] == "0.9.1"
    assert trace["steps"][0]["actions"] == previous["steps"][0]["actions"]
    assert trace["coverage"]["observed"] == trace["coverage"]["required"] == 2
    calls = [c for s in trace["steps"] for c in s.get("tool_calls", [])]
    assert len(calls) == 4
    assert sum(c["tool_error"] for c in calls) == 1
    engine = Copilot()
    for call in calls:
        action = call["action"]
        if call["tool_error"]:
            assert action["tool"] == "triage_issue"
            assert "customer message, not a recorded issue ID" in call["tool_result"][0]["text"]
            with pytest.raises(ValueError, match="customer message, not a recorded issue ID"):
                engine.triage_issue(**action["arguments"])
        else:
            assert getattr(engine, action["tool"])(**action["arguments"]) == call["tool_result"]
    assert not any("correction_feedback" in step for step in trace["steps"])
