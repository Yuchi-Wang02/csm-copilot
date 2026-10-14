from copy import deepcopy

import pytest

from csm_copilot.engine import Copilot
from csm_copilot.response_review import parse_grounded_actions, review_final


def example():
    engine = Copilot()
    calls, platforms = [], []
    for key in ("lantern_android", "lantern_ios"):
        ready = engine.check_readiness(key)
        for tool, output in (
            ("check_readiness", ready),
            ("draft_followup", engine.draft_followup(key)),
        ):
            calls.append(
                {
                    "action": {"tool": tool, "arguments": {"integration_id": key}},
                    "tool_error": False,
                    "tool_result": output,
                }
            )
        platforms.append(
            {
                "integration_id": key,
                "decision": ready["decision"],
                "unknown_checks": [c["id"] for c in ready["checks"] if c["status"] == "unknown"],
                "failed_checks": [c["id"] for c in ready["checks"] if c["status"] == "not_met"],
                "evidence_ids": sorted({e for c in ready["checks"] for e in c["evidence_ids"]}),
            }
        )
    return {
        "platforms": platforms,
        "nothing_sent": True,
        "launch_approved": False,
        "explanation": "A model-written explanation.",
    }, {"steps": [{"tool_calls": calls}]}


def test_checked_summary_preserves_failed_unknown_and_citations():
    claims, trace = example()
    report = review_final(claims, trace)
    assert report["status"] == "structured_fields_match"
    assert (
        "Non-test device verification: not_met [lantern_android_device_verified]"
        in report["checked_summary"]
    )
    assert "Platform currency approval: unknown [no applicable record]" in report["checked_summary"]
    assert "does not grant launch approval" in report["checked_summary"]


@pytest.mark.parametrize(
    "field,value",
    [
        ("decision", "checklist_complete"),
        ("unknown_checks", []),
        ("failed_checks", []),
        ("evidence_ids", ["lantern_ios_device_verified"]),
        ("evidence_ids", ["invented_source"]),
    ],
)
def test_plausible_wrong_fields_cannot_pass(field, value):
    claims, trace = example()
    claims["platforms"][0][field] = value
    report = review_final(claims, trace)
    assert report["status"] == "rejected"
    assert report["checked_summary"] is None
    assert any(i["field"] == f"lantern_android.{field}" for i in report["issues"])


def test_duplicate_source_and_omitted_platform_are_rejected():
    claims, trace = example()
    claims["platforms"][0]["evidence_ids"] *= 2
    claims["platforms"].pop()
    report = review_final(claims, trace)
    assert {i["code"] for i in report["issues"]} == {"scope", "mismatch"}


def test_duplicate_platform_cannot_cover_missing_platform():
    claims, trace = example()
    claims["platforms"][1] = deepcopy(claims["platforms"][0])
    assert review_final(claims, trace)["status"] == "rejected"


def test_model_claims_do_not_substitute_for_observed_tool_calls():
    claims, trace = example()
    trace["steps"][0]["tool_calls"][0]["tool_error"] = True
    report = review_final(claims, trace)
    assert any(i["code"] == "missing_tool_evidence" for i in report["issues"])


@pytest.mark.parametrize(
    "field,value", [("nothing_sent", False), ("launch_approved", True), ("nothing_sent", "true")]
)
def test_unsupported_boundaries_and_coerced_booleans_rejected(field, value):
    claims, trace = example()
    claims[field] = value
    assert review_final(claims, trace)["status"] == "rejected"


def test_matching_fields_never_certify_free_prose():
    claims, trace = example()
    claims["explanation"] = "Both platforms have full compliance and guaranteed revenue."
    report = review_final(claims, trace)
    assert report["status"] == "structured_fields_match"
    assert report["free_text_verification"] == "not_performed"
    assert report["human_review_required"] is True
    assert "guaranteed revenue" not in report["checked_summary"]


def test_legacy_prose_is_not_misrepresented_as_semantically_checked():
    report = review_final("Both are ready.", {"steps": []})
    assert report["status"] == "rejected"
    assert report["issues"][0]["code"] == "schema"
    assert report["free_text_verification"] == "not_performed"


def test_grounded_parser_preserves_final_for_review_but_rejects_mixed_batch():
    assert parse_grounded_actions('{"final":{"explanation":"raw"}}', set())[0]["final"] == {
        "explanation": "raw"
    }
    with pytest.raises(ValueError):
        parse_grounded_actions(
            '[{"final":{}},{"tool":"check_readiness","arguments":{}}]', {"check_readiness"}
        )
