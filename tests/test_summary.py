import copy
import subprocess
import sys

import pytest

from csm_copilot.demo import build_demo
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


def test_record_text_cannot_inject_terminal_controls_or_new_lines():
    workflow = build_demo()
    workflow["packets"][0]["selection"]["name"] = "Studio\nFAKE STATUS\x1b[2J"
    result = render_summary(workflow)
    assert "\x1b" not in result and "\nFAKE STATUS" not in result


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
