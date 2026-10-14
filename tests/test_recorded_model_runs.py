"""Integrity of published recordings, not a rerun or independent model-quality test."""

import hashlib
import json
from pathlib import Path

import pytest

from csm_copilot.engine import Copilot
from csm_copilot.host_protocol import trace_coverage

DIRECTORY = Path(__file__).resolve().parents[1] / "evidence/model-runs"


@pytest.mark.parametrize("name", ["qwen06-single", "qwen4-single", "qwen4-batch"])
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
