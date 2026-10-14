from csm_copilot.demo import build_demo
from csm_copilot.engine import Copilot


def test_passing_checks_change_the_question_without_closing_the_report():
    workflow = build_demo()
    branch = workflow["counterfactual"]
    assert branch["verified"]["decision"] == "checklist_complete"
    assert all(c["status"] == "met" for c in branch["verified"]["checks"])
    draft = branch["verified_followup"]
    assert draft["intent"] == "issue_status_review"
    assert draft["requests"] == []
    assert draft["issue_ids"] == ["issue_blank"]
    assert "whether it still occurs" in draft["body"]
    assert draft["contact_history_changed"] is False
    original = Copilot().get_account_context("acc_014")
    assert branch["verified_context"]["issues"] == original["issues"]
    assert branch["verified_context"]["account"] == original["account"]
    original_by_id = {e["id"]: e for e in original["evidence"]}
    for record in branch["verified_context"]["evidence"]:
        if record["id"] in original_by_id:
            assert record == original_by_id[record["id"]]


def test_test_records_are_scoped_and_original_packets_stay_unchanged():
    workflow = build_demo()
    branch = workflow["counterfactual"]
    for check in branch["verified"]["checks"]:
        if check["id"] in ("device_verified", "callback_verified"):
            assert check["evidence_ids"] == ["fresh_android_checks"]
    record = next(
        r for r in branch["verified_timing"]["records"] if r["id"] == "fresh_android_checks"
    )
    assert record["kind"] == "test_record"
    assert record["age_days"] == 0
    assert set(record["check_ids"]) == {"device_verified", "callback_verified"}
    packet = next(p for p in workflow["packets"] if p["selection"]["account_id"] == "acc_014")
    assert packet["context"] == Copilot().get_account_context("acc_014")
    assert packet["integrations"][0]["readiness"] == branch["before"]
    assert branch["before"]["decision"] == branch["after"]["decision"] == "blocked"
