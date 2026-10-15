"""Software checks with authored counterexamples, not model-quality evaluation."""

import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from lmformatenforcer import JsonSchemaParser

from csm_copilot.engine import Copilot
from csm_copilot.morning_review import morning_final_schema, review_morning_final


def test_explanation_checklist_supplies_no_fixture_identifiers_or_expected_answers():
    from csm_copilot.morning_review import MORNING_EXPLANATION_GUIDANCE

    engine = Copilot()
    for identifier in [*engine.accounts, *engine.integrations, *engine.issues]:
        assert identifier not in MORNING_EXPLANATION_GUIDANCE
    for fixture_answer in ("Lantern Games", "sdk_version", "redacted_logs", "contact_acc_014"):
        assert fixture_answer not in MORNING_EXPLANATION_GUIDANCE
    assert "does not verify your prose" in MORNING_EXPLANATION_GUIDANCE


def morning_example(engine=None):
    engine = engine or Copilot()
    calls = []

    def call(name, **args):
        result = getattr(engine, name)(**args)
        calls.append(
            {
                "action": {"tool": name, "arguments": args},
                "tool_error": False,
                "tool_result": result,
            }
        )
        return result

    queue = call("list_accounts")
    payload = {
        "selection": None,
        "platforms": [],
        "handoffs": [],
        "nothing_sent": True,
        "launch_approved": False,
        "explanation": "Authored test answer, not model inference. Nothing was sent.",
    }
    if queue["accounts"]:
        selected = queue["accounts"][0]
        context = call("get_account_context", account_id=selected["account_id"])
        payload["selection"] = {
            key: selected[key]
            for key in ("account_id", "contact_state", "days_since_contact", "days_to_launch")
        }
        payload["selection"]["contact_evidence_ids"] = context["account"]["contact_ids"]
        for integration in context["integrations"]:
            key = integration["id"]
            ready = call("check_readiness", integration_id=key)
            draft = call("draft_followup", integration_id=key, lang="en")
            payload["platforms"].append(
                {
                    "integration_id": key,
                    "decision": ready["decision"],
                    "unknown_checks": [
                        c["id"] for c in ready["checks"] if c["status"] == "unknown"
                    ],
                    "failed_checks": [c["id"] for c in ready["checks"] if c["status"] == "not_met"],
                    "evidence_ids": sorted({e for c in ready["checks"] for e in c["evidence_ids"]}),
                    "followup_intent": draft["intent"],
                }
            )
        for issue in context["issues"]:
            ticket = call("draft_ticket", issue_id=issue["id"])
            payload["handoffs"].append(
                {
                    "issue_id": issue["id"],
                    "integration_id": issue["integration_id"],
                    **{
                        key: ticket[key]
                        for key in ("missing_fields", "evidence_ids", "handoff_state", "root_cause")
                    },
                }
            )
    return deepcopy(payload), {"steps": [{"tool_calls": calls}]}


def decoder_accepts(schema, value):
    parser = JsonSchemaParser(schema)
    for character in json.dumps(value, ensure_ascii=False):
        if character not in parser.get_allowed_characters():
            return False
        parser = parser.add_character(character)
    return parser.can_end()


def test_morning_summary_preserves_selected_scope_states_next_actions_and_handoff():
    claims, trace = morning_example()
    original = deepcopy((claims, trace))
    result = review_morning_final(claims, trace)
    assert result["status"] == "structured_fields_match"
    summary = result["checked_summary"]
    for phrase in (
        "First account",
        "acc_014",
        "contact_acc_014",
        "unknown [no applicable record]",
        "not_met [lantern_android_device_verified]",
        "Review and send the evidence request",
        "Review the launch plan",
        "sdk_version, time_window, redacted_logs",
        "root cause: unconfirmed",
        "Nothing was sent",
    ):
        assert phrase in summary
    assert result["free_text_verification"] == "not_performed"
    assert (claims, trace) == original


@pytest.mark.parametrize(
    "section,field,value",
    [
        ("selection", "account_id", "acc_018"),
        ("selection", "days_since_contact", 0),
        ("selection", "days_to_launch", 4),
        ("selection", "contact_evidence_ids", ["msg_issue_blank"]),
        ("selection", "contact_evidence_ids", ["contact_acc_014", "contact_acc_014"]),
        (
            "platforms",
            "unknown_checks",
            ["currency_approved", "test_only_off", "callback_verified", "device_verified"],
        ),
        ("platforms", "failed_checks", []),
        ("platforms", "followup_intent", "launch_plan_review"),
        ("platforms", "evidence_ids", ["lantern_ios_device_verified"]),
        ("handoffs", "integration_id", "lantern_ios"),
        ("handoffs", "missing_fields", ["sdk_version"]),
        (
            "handoffs",
            "missing_fields",
            ["sdk_version", "time_window", "redacted_logs", "sdk_version"],
        ),
        ("handoffs", "evidence_ids", ["lantern_android_device_verified"]),
        ("handoffs", "handoff_state", "ready_for_human_review"),
        ("handoffs", "root_cause", "confirmed"),
    ],
)
def test_wrong_claims_are_rejected_without_rendering_a_checked_summary(section, field, value):
    claims, trace = morning_example()
    target = claims[section] if section == "selection" else claims[section][0]
    target[field] = value
    report = review_morning_final(claims, trace)
    assert report["status"] == "rejected" and report["checked_summary"] is None
    assert any(issue["field"].endswith("." + field) for issue in report["issues"])


@pytest.mark.parametrize(
    "fault",
    [
        "missing_platform",
        "duplicate_platform",
        "missing_handoff",
        "duplicate_handoff",
        "extra_handoff",
        "nothing_sent",
        "launch_approved",
        "string_bool",
        "extra_field",
        "numeric_bool",
        "overlong",
        "blank",
    ],
)
def test_final_scope_schema_boundaries_and_word_limit(fault):
    claims, trace = morning_example()
    if fault == "missing_platform":
        claims["platforms"].pop()
    elif fault == "duplicate_platform":
        claims["platforms"][1] = deepcopy(claims["platforms"][0])
    elif fault == "missing_handoff":
        claims["handoffs"] = []
    elif fault == "duplicate_handoff":
        claims["handoffs"] *= 2
    elif fault == "extra_handoff":
        claims["handoffs"][0]["issue_id"] = "foreign-issue"
    elif fault == "nothing_sent":
        claims["nothing_sent"] = False
    elif fault == "launch_approved":
        claims["launch_approved"] = True
    elif fault == "string_bool":
        claims["nothing_sent"] = "true"
    elif fault == "extra_field":
        claims["approved"] = True
    elif fault == "numeric_bool":
        claims["selection"]["days_to_launch"] = True
    elif fault == "overlong":
        claims["explanation"] = "word " * 221
    elif fault == "blank":
        claims["explanation"] = " \n "
    report = review_morning_final(claims, trace)
    assert report["status"] == "rejected" and report["checked_summary"] is None


@pytest.mark.parametrize(
    "fault",
    [
        "missing_queue",
        "missing_call",
        "failed_call",
        "duplicate_call",
        "wrong_context",
        "wrong_result_scope",
        "duplicate_source",
        "foreign_source",
        "wrong_contact_kind",
        "missing_check",
        "duplicate_check",
        "bad_intent",
        "sent_draft",
        "confirmed_cause",
        "wrong_ticket_source",
        "missing_action_text",
        "missing_name",
    ],
)
def test_missing_ambiguous_or_wrongly_scoped_tool_evidence_cannot_support_an_answer(fault):
    claims, trace = morning_example()
    calls = trace["steps"][0]["tool_calls"]
    context = calls[1]["tool_result"]
    if fault == "missing_queue":
        calls.pop(0)
    elif fault == "missing_call":
        calls.pop()
    elif fault == "failed_call":
        calls[-1]["tool_error"] = True
    elif fault == "duplicate_call":
        calls.append(deepcopy(calls[-1]))
    elif fault == "wrong_context":
        context["account"]["id"] = "foreign"
    elif fault == "wrong_result_scope":
        calls[2]["tool_result"]["integration_id"] = "lantern_ios"
    elif fault == "duplicate_source":
        context["evidence"].append(deepcopy(context["evidence"][0]))
    elif fault == "foreign_source":
        context["evidence"][0]["account_id"] = "foreign"
    elif fault == "wrong_contact_kind":
        context["evidence"][0]["kind"] = "test_record"
    elif fault == "missing_check":
        calls[2]["tool_result"]["checks"].pop()
    elif fault == "duplicate_check":
        calls[2]["tool_result"]["checks"].append(deepcopy(calls[2]["tool_result"]["checks"][0]))
    elif fault == "bad_intent":
        calls[3]["tool_result"]["intent"] = "approve_launch"
    elif fault == "sent_draft":
        calls[3]["tool_result"]["sent"] = True
    elif fault == "confirmed_cause":
        calls[-1]["tool_result"]["root_cause"] = "confirmed"
    elif fault == "wrong_ticket_source":
        calls[-1]["tool_result"]["evidence_ids"] = ["lantern_android_device_verified"]
    elif fault == "missing_action_text":
        calls[-1]["tool_result"].pop("next_action")
    elif fault == "missing_name":
        calls[0]["tool_result"]["accounts"][0].pop("name")
    report = review_morning_final(claims, trace)
    assert report["status"] == "rejected" and report["checked_summary"] is None
    assert any(issue["code"] == "invalid_or_incomplete" for issue in report["issues"])


def test_failed_call_can_be_retried_but_cannot_count_as_completed_work():
    claims, trace = morning_example()
    calls = trace["steps"][0]["tool_calls"]
    failed = deepcopy(calls[2])
    failed["tool_error"] = True
    failed["tool_result"] = {"error": "scripted failure"}
    calls.insert(2, failed)
    assert review_morning_final(claims, trace)["status"] == "structured_fields_match"


def test_empty_queue_unknown_contacts_and_other_accounts_use_observed_scope():
    data = Copilot().data.model_copy(deep=True)
    for account in data.accounts:
        account.stage = "live"
    claims, trace = morning_example(Copilot(data))
    assert claims["selection"] is None and not claims["platforms"] and not claims["handoffs"]
    assert decoder_accepts(morning_final_schema(), {"final": claims})
    assert "No accounts returned" in review_morning_final(claims, trace)["checked_summary"]
    data = Copilot().data.model_copy(deep=True)
    next(a for a in data.accounts if a.id == "acc_014").contact_ids = []
    claims, trace = morning_example(Copilot(data))
    assert claims["selection"]["days_since_contact"] is None
    assert decoder_accepts(morning_final_schema(), {"final": claims})
    assert review_morning_final(claims, trace)["status"] == "structured_fields_match"
    # Select Harbor first through its planned date, not by changing expected IDs in the reviewer.
    harbor = next(a for a in data.accounts if a.id == "acc_006")
    harbor.target_launch = data.as_of
    claims, trace = morning_example(Copilot(data))
    assert claims["selection"]["account_id"] == "acc_006"
    assert claims["handoffs"][0]["issue_id"] == "issue_callback"
    assert review_morning_final(claims, trace)["status"] == "structured_fields_match"


def test_decoder_schema_does_not_supply_or_certify_customer_answers():
    claims, trace = morning_example()
    schema = morning_final_schema()
    Draft202012Validator.check_schema(schema)
    assert "lantern" not in json.dumps(schema) and "acc_014" not in json.dumps(schema)
    assert decoder_accepts(schema, {"final": claims})
    claims["platforms"][0]["failed_checks"] = []
    assert Draft202012Validator(schema).is_valid({"final": claims})
    assert decoder_accepts(schema, {"final": claims})
    assert review_morning_final(claims, trace)["status"] == "rejected"
    assert not decoder_accepts(schema, {"final": "Old free-text format"})


def test_matching_fields_leave_unsupported_prose_unverified_and_preserve_old_recording():
    claims, trace = morning_example()
    claims["explanation"] = "Both launches are approved and revenue is guaranteed."
    report = review_morning_final(claims, trace)
    assert report["status"] == "structured_fields_match"
    assert report["free_text_verification"] == "not_performed" and report["human_review_required"]
    assert "revenue is guaranteed" not in report["checked_summary"]
    path = (
        Path(__file__).resolve().parents[1] / "evidence/model-runs/qwen4-morning-long-budget.json"
    )
    raw = path.read_bytes()
    recorded = json.loads(raw)
    assert review_morning_final(recorded["final"], recorded)["issues"][0]["code"] == "schema"
    correct, _ = morning_example()
    assert review_morning_final(correct, recorded)["status"] == "structured_fields_match"
    assert path.read_bytes() == raw
