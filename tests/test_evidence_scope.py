"""Regression cases for source ownership, check scope and handoff field integrity."""

import pytest
from pydantic import ValidationError

from csm_copilot.engine import Copilot
from csm_copilot.models import Dataset


@pytest.fixture
def data():
    return Copilot().data.model_dump(mode="json")


def test_ios_evidence_cannot_certify_android(data):
    data["integrations"][0]["facts"]["currency_approved"] = {
        "status": "met",
        "evidence_ids": ["lantern_ios_currency_approved"],
    }
    with pytest.raises(ValidationError, match="integration scope"):
        Dataset.model_validate(data)


def test_another_check_cannot_certify_currency(data):
    data["integrations"][0]["facts"]["currency_approved"] = {
        "status": "met",
        "evidence_ids": ["lantern_android_sdk_connected"],
    }
    with pytest.raises(ValidationError, match="check scope"):
        Dataset.model_validate(data)


def test_other_customer_contact_cannot_reset_followup_clock(data):
    data["accounts"][0]["contact_ids"] = ["contact_acc_011"]
    with pytest.raises(ValidationError, match="account scope"):
        Dataset.model_validate(data)


def test_other_issue_cannot_supply_ticket_source(data):
    data["issues"][0]["evidence_id"] = "msg_issue_callback"
    with pytest.raises(ValidationError, match="integration scope"):
        Dataset.model_validate(data)


@pytest.mark.parametrize(
    "key,value", [("app", "Wrong app"), ("platform", "iOS"), ("approved", "yes")]
)
def test_issue_details_cannot_override_identity_or_add_untracked_fields(data, key, value):
    data["issues"][0]["details"][key] = value
    with pytest.raises(ValidationError):
        Dataset.model_validate(data)


def test_blank_detail_remains_missing(data):
    data["issues"][0]["details"]["sdk_version"] = " \t\n "
    ticket = Copilot(Dataset.model_validate(data)).draft_ticket("issue_blank")
    assert "sdk_version" in ticket["missing_fields"]
    assert "sdk_version" not in ticket["fields"]


def test_unknown_check_name_cannot_silently_disappear(data):
    data["integrations"][0]["facts"]["curreny_approved"] = {"status": "unknown", "evidence_ids": []}
    with pytest.raises(ValidationError):
        Dataset.model_validate(data)


def test_claim_cannot_be_flipped_from_failed_to_passed(data):
    data["integrations"][0]["facts"]["device_verified"]["status"] = "met"
    with pytest.raises(ValidationError, match="conflicts with fact state"):
        Dataset.model_validate(data)


def test_disagreement_can_be_retained_without_inventing_a_winner(data):
    data["evidence"].append(
        {
            "id": "customer_says_device_works",
            "account_id": "acc_014",
            "integration_id": "lantern_android",
            "at": data["as_of"],
            "kind": "customer_report",
            "text": "Synthetic report: it works on my Android device.",
            "claims": {"device_verified": "met"},
        }
    )
    data["integrations"][0]["facts"]["device_verified"] = {
        "status": "unknown",
        "evidence_ids": ["lantern_android_device_verified", "customer_says_device_works"],
    }
    engine = Copilot(Dataset.model_validate(data))
    result = engine.check_readiness("lantern_android")
    check = next(c for c in result["checks"] if c["id"] == "device_verified")
    assert check["status"] == "unknown" and len(check["evidence_ids"]) == 2
    assert result["decision"] == "needs_evidence"
    assert "device_verified" in {
        r["check_id"] for r in engine.draft_followup("lantern_android")["requests"]
    }


def test_multiple_assertions_in_one_correctly_scoped_report(data):
    data["evidence"].append(
        {
            "id": "customer_confirms_settings",
            "account_id": "acc_014",
            "integration_id": "lantern_android",
            "at": data["as_of"],
            "kind": "customer_report",
            "text": "Synthetic report: currency approved; Test Only off.",
            "claims": {"currency_approved": "met", "test_only_off": "met"},
        }
    )
    for key in ("currency_approved", "test_only_off"):
        data["integrations"][0]["facts"][key] = {
            "status": "met",
            "evidence_ids": ["customer_confirms_settings"],
        }
    engine = Copilot(Dataset.model_validate(data))
    checks = {c["id"]: c for c in engine.check_readiness("lantern_android")["checks"]}
    assert checks["currency_approved"]["status"] == checks["test_only_off"]["status"] == "met"
    assert checks["device_verified"]["status"] == "not_met"


def test_unknown_with_correctly_scoped_evidence_stays_unknown(data):
    data["integrations"][0]["facts"]["device_verified"]["status"] = "unknown"
    checks = Copilot(Dataset.model_validate(data)).check_readiness("lantern_android")["checks"]
    assert next(c for c in checks if c["id"] == "device_verified")["status"] == "unknown"


def test_source_account_and_integration_must_agree_even_if_unreferenced(data):
    # Unreferenced records are validated too, so bad evidence cannot be parked for later reuse.
    data["evidence"].append(
        {
            "id": "orphan",
            "account_id": "acc_006",
            "integration_id": "lantern_android",
            "at": data["as_of"],
            "kind": "customer_report",
            "text": "Wrong customer context.",
        }
    )
    with pytest.raises(ValidationError, match="does not belong to its account"):
        Dataset.model_validate(data)


def test_contact_record_cannot_certify_technical_check(data):
    source = next(e for e in data["evidence"] if e["id"] == "contact_acc_014")
    source["claims"] = {"sdk_connected": "met"}
    with pytest.raises(ValidationError, match="scoped customer report or test record"):
        Dataset.model_validate(data)


def test_duplicate_references_do_not_inflate_evidence(data):
    data["integrations"][0]["facts"]["device_verified"]["evidence_ids"] *= 2
    with pytest.raises(ValidationError, match="Duplicate fact evidence"):
        Dataset.model_validate(data)


def test_details_are_normalized_without_losing_real_information(data):
    data["issues"][0]["details"]["sdk_version"] = " 14.1.0 "
    result = Copilot(Dataset.model_validate(data)).draft_ticket("issue_blank")
    assert result["fields"]["sdk_version"] == "14.1.0"
    assert result["fields"]["app"] == "Moon Garden" and result["fields"]["platform"] == "Android"
    assert result["field_sources"]["platform"] == {
        "source_kind": "integration_record",
        "source_id": "lantern_android",
    }
    assert result["field_sources"]["sdk_version"]["source_id"] == "msg_issue_blank"
