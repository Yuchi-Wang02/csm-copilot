"""Check the displayed repair against recorded outputs, not an independent quality score."""

import json
from copy import deepcopy
from pathlib import Path

import pytest

from csm_copilot.morning_review import review_morning_final
from scripts.build_model_replay import compare_morning_correction


def recording():
    path = Path(__file__).resolve().parents[1] / "evidence/model-runs/qwen4-morning-correction.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_comparison_preserves_actual_values_locations_and_unchanged_text():
    trace = recording()
    original = deepcopy(trace)
    comparison = compare_morning_correction(trace)
    assert (comparison["before_turn"], comparison["after_turn"]) == (8, 9)
    readiness, handoff, explanation = comparison["rows"]
    assert readiness["before"] == readiness["after"] + ["msg_issue_blank"]
    assert handoff["before"] == handoff["after"] == ["msg_issue_blank"]
    assert explanation["before"] == explanation["after"] == trace["final"]["explanation"]
    assert readiness["paths"] == [
        "steps[7].actions[0].final.platforms[0].evidence_ids",
        "steps[8].actions[0].final.platforms[0].evidence_ids",
    ]
    assert comparison["feedback"] == trace["steps"][7]["correction_feedback"]
    assert trace == original
    # Locate scope by ID rather than assuming the platform's array position.
    for step in trace["steps"][7:]:
        step["actions"][0]["final"]["platforms"].reverse()
        step["model_response"]["text"] = json.dumps(step["actions"][0])
    trace["final"]["platforms"].reverse()
    reordered = compare_morning_correction(trace)
    assert reordered["rows"][0]["paths"][0].endswith("platforms[1].evidence_ids")
    assert reordered["rows"][0]["before"] == readiness["before"]


@pytest.mark.parametrize(
    "fault", ["feedback", "model_text", "review", "scope", "extra_change", "missing_correction"]
)
def test_comparison_withholds_an_unsupported_or_misattributed_repair(fault):
    trace = recording()
    if fault == "feedback":
        trace["steps"][7]["correction_feedback"]["content"] = "Different feedback"
    elif fault == "model_text":
        trace["steps"][8]["model_response"]["text"] = '{"final": {}}'
    elif fault == "review":
        trace["steps"][7]["response_review"]["issues"] = []
    elif fault == "scope":
        final = trace["steps"][8]["actions"][0]["final"]
        final["platforms"][0]["integration_id"] = "lantern_ios"
        trace["steps"][8]["model_response"]["text"] = json.dumps({"final": final})
    elif fault == "extra_change":
        final = trace["steps"][8]["actions"][0]["final"]
        final["explanation"] = "A different explanation."
        trace["steps"][8]["model_response"]["text"] = json.dumps({"final": final})
        trace["steps"][8]["response_review"] = review_morning_final(final, trace)
        trace["final"] = deepcopy(final)
        trace["response_review"] = deepcopy(trace["steps"][8]["response_review"])
    else:
        del trace["steps"][7]["correction_feedback"]
    with pytest.raises(ValueError, match="Correction comparison requires"):
        compare_morning_correction(trace)
