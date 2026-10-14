from copy import deepcopy

from csm_copilot.engine import Copilot
from csm_copilot.friction import render_friction_brief
from csm_copilot.models import Dataset


def theme(digest, key):
    return next(t for t in digest["themes"] if t["check_id"] == key)


def test_snapshot_counts_and_evidence_states_are_separate():
    result = Copilot().friction_digest()
    assert result["cohort_account_count"] == 4
    assert result["cohort_integration_count"] == 5
    device = theme(result, "device_verified")
    assert device["affected_account_ids"] == ["acc_014", "acc_018"]
    assert device["unknown_integration_count"] == 1
    assert device["failed_integration_count"] == 1
    assert device["recurring_across_accounts"] is True
    assert theme(result, "currency_approved")["recurring_across_accounts"] is False


def test_managed_callbacks_do_not_inflate_denominator_or_gaps():
    callback = theme(Copilot().friction_digest(), "callback_verified")
    assert callback["applicable_integration_ids"] == [
        "harbor_android",
        "lantern_android",
        "lantern_ios",
    ]
    assert callback["affected_integration_count"] == 2
    assert callback["applicable_integration_count"] == 3
    assert callback["unknown_integration_count"] == callback["failed_integration_count"] == 1


def test_two_platforms_of_one_account_do_not_become_two_customers():
    data = Copilot().data.model_dump(mode="json")
    ios = next(i for i in data["integrations"] if i["id"] == "lantern_ios")
    ios["facts"]["currency_approved"] = {"status": "unknown", "evidence_ids": []}
    approval = theme(Copilot(Dataset.model_validate(data)).friction_digest(), "currency_approved")
    assert approval["affected_integration_count"] == 2
    assert approval["affected_account_count"] == 1
    assert approval["recurring_across_accounts"] is False


def test_duplicate_evidence_does_not_become_a_second_observation():
    data = Copilot().data.model_dump(mode="json")
    record = deepcopy(
        next(e for e in data["evidence"] if e["id"] == "lantern_android_device_verified")
    )
    record["id"] = "duplicate_report"
    data["evidence"].append(record)
    android = next(i for i in data["integrations"] if i["id"] == "lantern_android")
    android["facts"]["device_verified"]["evidence_ids"].append(record["id"])
    device = theme(Copilot(Dataset.model_validate(data)).friction_digest(), "device_verified")
    assert device["affected_integration_count"] == 2
    assert device["failed_integration_count"] == 1


def test_sources_are_integration_scoped_and_unknowns_have_no_fabricated_records():
    result = Copilot().friction_digest()
    for item in result["themes"]:
        for member in item["members"]:
            assert member["evidence_ids"] == [r["id"] for r in member["source_records"]]
            for record in member["source_records"]:
                assert record["integration_id"] == member["integration_id"]
                assert record["account_id"] == member["account_id"]
    meadow = next(
        m
        for m in theme(result, "device_verified")["members"]
        if m["integration_id"] == "meadow_ios"
    )
    assert meadow["source_records"] == []


def test_live_cohort_is_explicit_and_not_contact_queue_dependent():
    default = Copilot().friction_digest()
    expanded = Copilot().friction_digest(include_live=True)
    assert "acc_011" in default["cohort_account_ids"]  # Recently contacted still belongs.
    assert "acc_009" not in default["cohort_account_ids"]
    assert "acc_009" in expanded["cohort_account_ids"]
    assert expanded["cohort_account_count"] == 5
    assert expanded["cohort_integration_count"] == 6
    assert theme(expanded, "device_verified")["applicable_integration_count"] == 6
    assert theme(expanded, "callback_verified")["applicable_integration_count"] == 3


def test_empty_cohort_does_not_invent_patterns_or_divide_by_zero():
    data = Copilot().data.model_dump(mode="json")
    for account in data["accounts"]:
        account["stage"] = "live"
    result = Copilot(Dataset.model_validate(data)).friction_digest()
    assert result["cohort_account_count"] == result["cohort_integration_count"] == 0
    assert result["themes"] == []
    assert "No scoped checklist friction found" in render_friction_brief(result)


def test_repeated_digest_is_read_only_and_input_order_independent():
    engine = Copilot()
    before = engine.data.model_dump(mode="json")
    first = engine.friction_digest()
    assert first == engine.friction_digest()
    assert engine.data.model_dump(mode="json") == before
    before["accounts"].reverse()
    before["integrations"].reverse()
    assert first == Copilot(Dataset.model_validate(before)).friction_digest()


def test_export_exposes_hypotheses_limits_and_source_text_safely():
    result = Copilot().friction_digest()
    device = theme(result, "device_verified")
    device["members"][0]["account_name"] = "<script>alert(1)</script> [link](https://example.com)"
    output = render_friction_brief(result)
    assert "<script>" not in output
    assert "[link](" not in output
    assert "No applicable record" in output
    assert r"lantern\_android\_device\_verified" in output
    assert "Proposed owner" in output and "Validation step" in output
    assert "not a weekly trend" in output
    assert "themes overlap" in output


def test_friction_counts_are_not_added_as_unique_accounts():
    result = Copilot().friction_digest()
    affected = {a for t in result["themes"] for a in t["affected_account_ids"]}
    assert len(affected) == 3
    assert sum(t["affected_account_count"] for t in result["themes"]) == 6
    assert "must not be added" in result["counting_policy"]
