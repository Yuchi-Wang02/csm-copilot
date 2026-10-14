import copy
import subprocess
import sys

import pytest

from csm_copilot.demo import build_demo
from csm_copilot.engine import Copilot
from csm_copilot.summary import render_summary


def test_summary_preserves_platform_gaps_and_handoff_missingness():
    result = render_summary(build_demo())
    assert "Queue: 3 accounts, 4 platforms" in result
    assert (
        result.index("Lantern Games") < result.index("Meadow Works") < result.index("Harbor Studio")
    )
    assert "Moon Garden / Android: blocked" in result
    assert "device_verified: not_met [lantern_android_device_verified]" in result
    assert "callback_verified: unknown [no applicable record]" in result
    assert "Moon Garden / iOS: checklist_complete" in result
    assert "missing: sdk_version, time_window, redacted_logs" in result
    assert "Handoff issue_callback:" in result
    assert "not launch approval or issue resolution" in result


def test_summary_is_repeatable_and_excludes_the_synthetic_update_branch():
    workflow = build_demo()
    before = copy.deepcopy(workflow)
    result = render_summary(workflow)
    assert result == render_summary(workflow)
    assert workflow == before
    assert "reply_android_settings" not in result and "fresh_android_checks" not in result
    assert "Pine Pixel" not in result and "Orbit Play" not in result
    assert "no model inference" in result and "nothing sent" in result


def test_unknown_contact_and_absent_handoff_do_not_become_success_claims():
    workflow = build_demo()
    workflow["packets"][0]["selection"]["days_since_contact"] = None
    workflow["packets"][0]["tickets"] = []
    result = render_summary(workflow)
    assert "Last contact: unknown" in result
    assert "issue_blank: no handoff draft in this packet" in result
    workflow["packets"] = []
    assert "No accounts in this review queue." in render_summary(workflow)


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("conflicting", [False, True])
def test_summary_withholds_duplicate_handoffs_without_selecting_by_order(reverse, conflicting):
    workflow = build_demo()
    packet = next(p for p in workflow["packets"] if p["context"]["account"]["id"] == "acc_014")
    duplicate = copy.deepcopy(packet["tickets"][0])
    if conflicting:
        duplicate["handoff_state"] = "conflicting_state_must_not_be_selected"
        duplicate["suggested_owner"] = "conflicting_owner_must_not_be_selected"
    packet["tickets"].append(duplicate)
    if reverse:
        packet["tickets"].reverse()
    before = copy.deepcopy(workflow)

    result = render_summary(workflow)

    assert "issue_blank: handoff unavailable; 2 matching drafts. Review the packet." in result
    assert "Handoff issue_blank:" not in result
    assert "conflicting_state_must_not_be_selected" not in result
    assert "conflicting_owner_must_not_be_selected" not in result
    assert "Moon Garden / Android: blocked" in result
    assert "Handoff issue_callback: needs_information" in result
    assert workflow == before


def test_record_text_cannot_inject_terminal_controls_or_new_lines():
    workflow = build_demo()
    workflow["packets"][0]["selection"]["name"] = "Studio\nFAKE STATUS\x1b[2J"
    result = render_summary(workflow)
    assert "\x1b" not in result and "\nFAKE STATUS" not in result


@pytest.mark.parametrize("draft_count", [0, 1, 2])
def test_recorded_issue_summary_survives_missing_or_ambiguous_handoffs(draft_count):
    workflow = build_demo()
    packet = workflow["packets"][0]
    issue = packet["context"]["issues"][0]
    issue["summary"] = "Recorded Android symptom; confirm current status."
    ticket = copy.deepcopy(packet["tickets"][0])
    ticket["title"] = "Draft title must not replace the recorded issue summary"
    packet["tickets"] = [copy.deepcopy(ticket) for _ in range(draft_count)]
    before = copy.deepcopy(workflow)

    result = render_summary(workflow)
    android, ios = result.split("Moon Garden / iOS:", 1)

    assert (
        "Recorded issue issue_blank: Recorded Android symptom; confirm current status." in android
    )
    assert "Recorded Android symptom" not in ios
    assert "Draft title must not replace" not in result
    assert result.count("Recorded issue issue_blank:") == 1
    assert "Recorded issue issue_callback:" in result
    assert workflow == before


def test_recorded_issue_summary_is_literal_single_line_terminal_text():
    workflow = build_demo()
    issue = workflow["packets"][0]["context"]["issues"][0]
    issue["summary"] = "客户报告\nFAKE APPROVAL\x1b[2J\r\tstill a recorded statement"
    before = copy.deepcopy(workflow)

    result = render_summary(workflow)

    assert (
        "Recorded issue issue_blank: 客户报告 FAKE APPROVAL [2J still a recorded statement"
        in result
    )
    assert "\x1b" not in result and "\nFAKE APPROVAL" not in result
    assert "\r" not in result and "\t" not in result
    assert workflow == before


@pytest.mark.parametrize("complete", [False, True])
def test_summary_prioritizes_scope_over_generic_field_completeness(complete):
    data = Copilot().data.model_copy(deep=True)
    issue = next(i for i in data.issues if i.id == "issue_callback")
    issue.summary = "Please explain invoicing."
    record = next(e for e in data.evidence if e.id == issue.evidence_id)
    record.text = issue.summary
    if complete:
        for field in type(issue.details).model_fields:
            setattr(issue.details, field, "Recorded placeholder; not reviewed")
    engine = Copilot(data)
    ticket = engine.draft_ticket(issue.id)
    assert ticket["handoff_state"] == "needs_scope"
    assert ticket["collection_requests"] == []
    workflow = build_demo()
    packet = next(
        p for p in workflow["packets"] if p["context"]["account"]["id"] == record.account_id
    )
    packet["context"] = engine.get_account_context(record.account_id)
    packet["tickets"] = [ticket]
    before = copy.deepcopy(workflow)

    result = render_summary(workflow)
    handoff = result.split("Handoff issue_callback:", 1)[1].split("\n\n", 1)[0]

    assert "needs_scope" in handoff
    assert "Scope first: generic field completeness does not establish the request." in handoff
    assert ticket["next_action"] in handoff
    assert ticket["suggested_owner"] in handoff
    assert "missing:" not in handoff
    assert "reproduction_steps" not in handoff and "redacted_logs" not in handoff
    assert "Handoff issue_blank: needs_information; missing:" in result
    assert workflow == before


def test_summary_cli_stdout_and_file_match_the_original_workflow(tmp_path):
    command = [sys.executable, "-m", "csm_copilot.demo", "--format", "summary"]
    expected = render_summary(build_demo()).encode("utf-8")
    result = subprocess.run(command, capture_output=True, timeout=20)
    assert result.returncode == 0, result.stderr
    assert result.stdout == expected
    target = tmp_path / "summary.txt"
    result = subprocess.run(command + ["--output", str(target)], capture_output=True, timeout=20)
    assert result.returncode == 0, result.stderr
    assert target.read_bytes() == expected


@pytest.mark.parametrize("extra", [["--lang", "zh"], ["--integration", "lantern_android"]])
def test_incompatible_summary_options_do_not_write_a_file(tmp_path, extra):
    target = tmp_path / "summary.txt"
    result = subprocess.run(
        [sys.executable, "-m", "csm_copilot.demo", "--format", "summary", "--output", str(target)]
        + extra,
        capture_output=True,
        timeout=20,
    )
    assert result.returncode == 2
    assert not target.exists()
