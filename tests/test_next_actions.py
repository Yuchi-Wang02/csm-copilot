import pytest

from csm_copilot.engine import Copilot
from csm_copilot.models import Dataset


@pytest.mark.parametrize("lang", ["en", "zh"])
def test_complete_checklist_does_not_request_unspecified_updates(lang):
    draft = Copilot().draft_followup("lantern_ios", lang)
    assert draft["requests"] == []
    assert "when you expect to share them" not in draft["body"]
    assert "收到后" not in draft["body"]
    assert draft["intent"] == "launch_plan_review"


@pytest.mark.parametrize("lang", ["en", "zh"])
def test_live_account_gets_a_post_launch_followup(lang):
    draft = Copilot().draft_followup("pine_ios", lang)
    assert draft["intent"] == "post_launch_checkin"
    assert "Launch timing" not in draft["body"]
    assert "上线时间" not in draft["body"]


def test_complete_handoff_moves_to_review():
    data = Copilot().data.model_dump(mode="json")
    data["issues"][0]["details"].update(
        {
            "sdk_version": "synthetic-version-2",
            "time_window": "2026-10-09 08:30–09:00 UTC",
            "redacted_logs": "Synthetic redacted test log: content request returned empty.",
        }
    )
    result = Copilot(Dataset.model_validate(data)).draft_ticket("issue_blank")
    assert result["missing_fields"] == []
    assert result["handoff_state"] == "ready_for_human_review"
    assert "Request missing evidence" not in result["next_action"]
    assert result["sent"] is False


def test_recorded_issue_is_not_silently_closed_by_a_complete_checklist():
    data = Copilot().data.model_dump(mode="json")
    data["issues"].append(
        {
            "id": "prior_ios_issue",
            "integration_id": "lantern_ios",
            "summary": "Previously reported blank offerwall.",
            "evidence_id": "prior_ios_report",
            "details": {},
        }
    )
    data["evidence"].append(
        {
            "id": "prior_ios_report",
            "account_id": "acc_014",
            "integration_id": "lantern_ios",
            "at": "2026-10-08T09:00:00+00:00",
            "kind": "customer_report",
            "text": "Synthetic report: Offerwall was blank yesterday.",
        }
    )
    draft = Copilot(Dataset.model_validate(data)).draft_followup("lantern_ios")
    assert draft["intent"] == "issue_status_review"
    assert draft["issue_ids"] == ["prior_ios_issue"]
    assert "prior_ios_report" in draft["evidence_ids"]


def test_incomplete_checklist_keeps_specific_evidence_requests():
    draft = Copilot().draft_followup("lantern_android")
    assert draft["intent"] == "evidence_request"
    assert {r["check_id"] for r in draft["requests"]} == {
        "currency_approved",
        "test_only_off",
        "device_verified",
        "callback_verified",
    }
    assert draft["contact_history_changed"] is False
