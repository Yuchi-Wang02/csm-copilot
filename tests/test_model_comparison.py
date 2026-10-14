"""Check comparison facts without treating reviewed prose as independently validated."""

import json
import runpy
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
compare = runpy.run_path(str(ROOT / "scripts/build_model_replay.py"))["compare_handoffs"]
compare_claims = runpy.run_path(str(ROOT / "scripts/build_model_replay.py"))["compare_batch_claims"]


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


def batch_sources():
    directory = ROOT / "evidence/model-runs"
    trace = json.loads((directory / "qwen4-batch.json").read_text(encoding="utf-8"))
    review = json.loads((directory / "review.json").read_text(encoding="utf-8"))
    findings = next(run["findings"] for run in review["runs"] if run["id"] == "qwen4-batch")
    return trace, findings


def test_claim_cards_extract_exact_historical_values_and_preserve_inputs():
    trace, findings = batch_sources()
    before = deepcopy((trace, findings))
    rows = compare_claims(trace, findings)
    assert [r["claim"] for r in rows] == ["iOS's full compliance", "Android's missing evidence"]
    assert [f["value"] for f in rows[0]["fields"]] == [
        "checklist_complete",
        "A scoped evidence checklist, not a Unity launch approval or a fill guarantee.",
    ]
    assert [f["value"] for f in rows[1]["fields"]] == [
        "not_met",
        ["lantern_android_device_verified"],
    ]
    assert rows[0]["fields"][0]["path"] == "steps[0].tool_calls[1].tool_result.decision"
    assert rows[1]["fields"][0]["path"] == "steps[0].tool_calls[0].tool_result.checks[4].status"
    assert (trace, findings) == before


def test_claim_source_locations_follow_recorded_order_not_assumed_positions():
    trace, findings = batch_sources()
    trace["steps"][0]["tool_calls"].reverse()
    for call in trace["steps"][0]["tool_calls"]:
        if call["action"]["tool"] == "check_readiness":
            call["tool_result"]["checks"].reverse()
    rows = compare_claims(trace, findings)
    assert rows[0]["source_label"] == "Turn 1 · call 3 · lantern_ios"
    assert rows[1]["fields"][0]["path"] == "steps[0].tool_calls[3].tool_result.checks[1].status"


@pytest.mark.parametrize("damage", ["quote", "duplicate_call", "scope", "error", "missing_check"])
def test_claim_comparison_rejects_missing_or_ambiguous_historical_sources(damage):
    trace, findings = batch_sources()
    calls = trace["steps"][0]["tool_calls"]
    if damage == "quote":
        trace["final"] = "A different answer."
    elif damage == "duplicate_call":
        calls.append(deepcopy(calls[1]))
    elif damage == "scope":
        calls[1]["tool_result"]["integration_id"] = "lantern_android"
    elif damage == "error":
        calls[1]["tool_error"] = True
    else:
        calls[0]["tool_result"]["checks"] = []
    with pytest.raises(ValueError, match="Claim comparison requires"):
        compare_claims(trace, findings)
