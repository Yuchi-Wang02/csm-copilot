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


def test_callback_handoff_recording_matches_actual_tools_without_approving_prose():
    trace = json.loads((DIRECTORY / "qwen4-callback-handoff.json").read_text(encoding="utf-8"))
    assert trace["task_id"] == "callback_handoff"
    assert trace["coverage"]["observed"] == trace["coverage"]["required"] == 2
    engine = Copilot()
    calls = [c for step in trace["steps"] for c in step.get("tool_calls", [])]
    assert len(calls) == 4
    for call in calls:
        action = call["action"]
        assert getattr(engine, action["tool"])(**action["arguments"]) == call["tool_result"]
    assert not any("correction_feedback" in step for step in trace["steps"])
