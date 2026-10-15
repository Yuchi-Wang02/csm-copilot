"""Trace provenance for authored omission comparisons, not model-quality scoring."""

import json
import re
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.build_model_replay import compare_explanation_actions


def recording():
    path = Path(__file__).resolve().parents[1] / (
        "evidence/model-runs/qwen4-morning-explanation-checklist.json"
    )
    return json.loads(path.read_text(encoding="utf-8"))


def test_explanation_comparison_quotes_actual_drafts_and_resolvable_locations():
    trace = recording()
    original = deepcopy(trace)
    rows = compare_explanation_actions(trace)
    assert len(rows) == 3
    for row in rows:
        assert row["claim"] in trace["final"]["explanation"]
        for field in row["fields"]:
            value = trace
            for part in re.findall(r"[a-z_]+|\d+", field["path"]):
                value = value[int(part)] if part.isdigit() else value[part]
            assert field["value"] == value
    assert rows[0]["fields"][1]["value"].startswith("Review and send the evidence request")
    assert rows[1]["fields"][1]["value"].startswith("Review the launch plan")
    assert "secrets removed" in rows[2]["fields"][-1]["value"]
    assert trace == original
    rows[0]["fields"][2]["value"].append("display-only")
    assert trace == original


@pytest.mark.parametrize(
    "fault", ["excerpt", "raw_answer", "duplicate", "draft_scope", "tool_error", "message"]
)
def test_explanation_comparison_refuses_missing_or_conflicting_provenance(fault):
    trace = recording()
    if fault == "excerpt":
        trace["final"]["explanation"] = "Different explanation"
        trace["steps"][-1]["actions"] = [{"final": trace["final"]}]
        trace["steps"][-1]["model_response"]["text"] = json.dumps({"final": trace["final"]})
    elif fault == "raw_answer":
        trace["steps"][-1]["model_response"]["text"] = '{"final": {}}'
    elif fault == "duplicate":
        trace["steps"][4]["tool_calls"] *= 2
    elif fault == "draft_scope":
        trace["steps"][4]["tool_calls"][0]["tool_result"]["draft_id"] = "another-draft"
    elif fault == "tool_error":
        trace["steps"][4]["tool_calls"][0]["tool_error"] = True
    elif fault == "message":
        trace["steps"][4]["tool_calls"][0]["result_message"]["content"] = "Different tool result"
    with pytest.raises(ValueError, match="Explanation comparison"):
        compare_explanation_actions(trace)
