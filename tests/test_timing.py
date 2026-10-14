"""Snapshot-relative dates are descriptive, never an expiry or latest-wins policy."""

from copy import deepcopy

import pytest

from csm_copilot.demo import build_demo
from csm_copilot.engine import Copilot
from csm_copilot.timing import evidence_timing


@pytest.mark.parametrize("conflicting_date", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
def test_ambiguous_scoped_dates_are_withheld_regardless_of_record_order(conflicting_date, reverse):
    engine = Copilot()
    readiness = engine.check_readiness("lantern_android")
    context = engine.get_account_context("acc_014")
    identifier = "lantern_android_device_verified"
    duplicate = deepcopy(next(r for r in context["evidence"] if r["id"] == identifier))
    if conflicting_date:
        duplicate["at"] = "2026-10-14T09:00:00Z"
    context["evidence"].append(duplicate)
    if reverse:
        context["evidence"].reverse()
    original = deepcopy((readiness, context))

    timing = evidence_timing(readiness, context)

    assert timing["unavailable_ids"] == [identifier]
    assert identifier not in {r["id"] for r in timing["records"]}
    assert len(timing["records"]) == 2
    assert readiness["decision"] == "blocked"
    assert (readiness, context) == original


@pytest.mark.parametrize("wrong_scope", ["account_id", "integration_id"])
@pytest.mark.parametrize("reverse", [False, True])
def test_unrelated_same_id_record_cannot_hide_one_unique_scoped_date(wrong_scope, reverse):
    engine = Copilot()
    readiness = engine.check_readiness("lantern_android")
    context = engine.get_account_context("acc_014")
    baseline = evidence_timing(readiness, context)
    unrelated = deepcopy(
        next(r for r in context["evidence"] if r["id"] == "lantern_android_device_verified")
    )
    unrelated[wrong_scope] = "unrelated"
    unrelated["at"] = "not a timestamp in this platform's evidence"
    context["evidence"].append(unrelated)
    if reverse:
        context["evidence"].reverse()
    original = deepcopy((readiness, context))

    assert evidence_timing(readiness, context) == baseline
    assert (readiness, context) == original


def test_update_has_one_new_source_but_retains_the_older_failed_device_record():
    comparison = build_demo()["counterfactual"]
    before, after = comparison["before_timing"], comparison["after_timing"]
    record = next(r for r in after["records"] if r["id"] == "reply_android_settings")
    assert record["age_days"] == 0
    assert record["check_ids"] == ["currency_approved", "test_only_off"]
    device_before = next(r for r in before["records"] if "device_verified" in r["check_ids"])
    device_after = next(r for r in after["records"] if "device_verified" in r["check_ids"])
    assert device_before == device_after
    assert device_after["age_days"] > record["age_days"]
    assert comparison["before"]["decision"] == comparison["after"]["decision"] == "blocked"
    assert all(r["id"] != record["id"] for r in before["records"])


def test_age_uses_elapsed_time_and_timezone_offsets_without_mutating_or_expiring_evidence():
    engine = Copilot()
    readiness = engine.check_readiness("lantern_ios")
    context = engine.get_account_context("acc_014")
    target = next(
        r for r in context["evidence"] if r["id"] == readiness["checks"][0]["evidence_ids"][0]
    )
    target["at"] = "2026-10-13T05:00:00-04:00"
    original = deepcopy((readiness, context))
    timing = evidence_timing(readiness, context)
    assert next(r for r in timing["records"] if r["id"] == target["id"])["age_days"] == 1
    assert (readiness, context) == original
    target["at"] = "2020-01-01T00:00:00Z"
    assert evidence_timing(readiness, context)["records"][0]["age_days"] > 2000
    assert readiness["decision"] == "checklist_complete"


@pytest.mark.parametrize("scope", ["missing", "account", "integration"])
def test_unavailable_or_misscoped_source_has_no_invented_timestamp(scope):
    engine = Copilot()
    readiness = engine.check_readiness("lantern_android")
    context = engine.get_account_context("acc_014")
    identifier = next(c["evidence_ids"][0] for c in readiness["checks"] if c["evidence_ids"])
    record = next(r for r in context["evidence"] if r["id"] == identifier)
    if scope == "missing":
        context["evidence"].remove(record)
    else:
        record[f"{scope}_id"] = "other"
    timing = evidence_timing(readiness, context)
    assert identifier in timing["unavailable_ids"]
    assert identifier not in [r["id"] for r in timing["records"]]


@pytest.mark.parametrize("at", ["2026-10-15T00:00:00Z", "2026-10-10T00:00:00"])
def test_invalid_source_dates_are_not_rendered_as_zero_age(at):
    engine = Copilot()
    readiness = engine.check_readiness("lantern_ios")
    context = engine.get_account_context("acc_014")
    identifier = readiness["checks"][0]["evidence_ids"][0]
    next(r for r in context["evidence"] if r["id"] == identifier)["at"] = at
    with pytest.raises(ValueError, match="aware timestamp"):
        evidence_timing(readiness, context)


def test_timeline_excludes_contact_and_issue_only_records_and_keeps_empty_checks_empty():
    engine = Copilot()
    readiness = engine.check_readiness("lantern_android")
    context = engine.get_account_context("acc_014")
    timing = evidence_timing(readiness, context)
    expected = {eid for check in readiness["checks"] for eid in check["evidence_ids"]}
    assert {r["id"] for r in timing["records"]} == expected
    assert all(r["kind"] != "contact_record" for r in timing["records"])
    for check in readiness["checks"]:
        check["evidence_ids"] = []
    assert evidence_timing(readiness, context)["records"] == []
