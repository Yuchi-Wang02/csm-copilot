"""Check comparison facts without treating reviewed prose as independently validated."""

import json
import runpy
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
compare = runpy.run_path(str(ROOT / "scripts/build_model_replay.py"))["compare_handoffs"]


def recordings():
    return [
        {
            "id": identifier,
            "label": identifier,
            "trace": json.loads(
                (ROOT / f"evidence/model-runs/{identifier}.json").read_text(encoding="utf-8")
            ),
        }
        for identifier in ("qwen4-callback-handoff", "qwen4-callback-input-guard")
    ]


def test_comparison_separates_required_coverage_from_all_attempts_and_errors():
    runs = recordings()
    original = deepcopy(runs)
    result = compare(runs)
    assert [item["required_actions"] for item in result["attempts"]] == ["2 / 2", "2 / 2"]
    assert [item["attempted_calls"] for item in result["attempts"]] == [4, 4]
    assert [item["tool_errors"] for item in result["attempts"]] == [0, 1]
    assert [item["triage_result"] for item in result["attempts"]] == ["Accepted", "Rejected"]
    assert result["controls"]["Initial action batch"] is True
    assert result["controls"]["System message including tool descriptions"] is False
    assert runs == original


def test_changed_controls_are_reported_instead_of_assumed_identical():
    runs = recordings()
    runs[1]["trace"]["task"] = "Different task"
    runs[1]["trace"]["runtime"]["seed"] = 99
    runs[1]["trace"]["steps"][0]["actions"] = []
    controls = compare(runs)["controls"]
    assert controls["Task text"] is False
    assert controls["Recorded sampling settings"] is False
    assert controls["Initial action batch"] is False


def test_missing_recording_is_not_silently_replaced_by_another_attempt():
    with pytest.raises(ValueError, match="Both callback"):
        compare(recordings()[:1])
