import copy
import os
import subprocess
import sys

import pytest

from csm_copilot.brief import render_review_brief
from csm_copilot.demo import build_demo


def test_brief_carries_all_selected_accounts_and_platform_states():
    brief = render_review_brief(build_demo())
    for name in ("Lantern Games", "Meadow Works", "Harbor Studio"):
        assert name in brief
    assert "## Pine Pixel" not in brief and "## Orbit Play" not in brief
    assert "### Moon Garden / Android" in brief and "### Moon Garden / iOS" in brief
    assert "blocked" in brief and r"checklist\_complete" in brief
    assert "Nothing was sent or submitted" in brief
    assert "not evidence of a live model run" in brief


def test_brief_preserves_missing_fields_and_evidence_references():
    brief = render_review_brief(build_demo())
    assert r"sdk\_version, time\_window, redacted\_logs" in brief
    assert r"msg\_issue\_blank" in brief
    assert "## Evidence index" in brief
    assert "https://docs.unity.com/en-us/grow/offerwall/monetization/other/faq" in brief


def test_chinese_export_changes_client_drafts_but_preserves_review_context():
    workflow = build_demo()
    brief = render_review_brief(workflow, "zh")
    assert "Lantern Games 团队好" in brief
    assert "CSM Copilot — Morning review brief" in brief
    assert "Client draft language: Chinese" in brief
    assert "根据现有记录" in brief


def test_export_is_repeatable_and_read_only():
    workflow = build_demo()
    original = copy.deepcopy(workflow)
    assert render_review_brief(workflow) == render_review_brief(workflow)
    assert workflow == original


def test_customer_markup_cannot_become_html_or_a_link_in_the_brief():
    workflow = build_demo()
    workflow["packets"][0]["context"]["evidence"][0]["text"] = (
        "<script>alert(1)</script> | [click](javascript:alert(1))"
    )
    brief = render_review_brief(workflow)
    assert "<script>" not in brief
    assert "[click](javascript:" not in brief
    assert r"\| \[click\]" in brief


def test_cli_writes_the_same_readable_export(tmp_path):
    output = tmp_path / "brief.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "csm_copilot.demo",
            "--format",
            "markdown",
            "--lang",
            "en",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
    assert output.read_text(encoding="utf-8") == render_review_brief(build_demo())


def test_invalid_export_language_is_rejected():
    with pytest.raises(ValueError, match="lang must"):
        render_review_brief(build_demo(), "fr")


def test_chinese_stdout_export_is_utf8_even_with_ascii_console_encoding():
    result = subprocess.run(
        [sys.executable, "-m", "csm_copilot.demo", "--format", "markdown", "--lang", "zh"],
        capture_output=True,
        env={**os.environ, "PYTHONIOENCODING": "ascii"},
        timeout=20,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    assert "Lantern Games 团队好" in result.stdout.decode("utf-8")
