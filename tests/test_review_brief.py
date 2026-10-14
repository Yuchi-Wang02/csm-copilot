import copy
import os
import subprocess
import sys
from pathlib import Path

import pytest

from csm_copilot.brief import render_review_brief
from csm_copilot.demo import build_demo


@pytest.mark.parametrize("lang", ["en", "zh"])
def test_generated_morning_briefs_match_renderer_bytes_on_every_platform(lang):
    root = Path(__file__).resolve().parents[1]
    expected = render_review_brief(build_demo(), lang).encode("utf-8")
    for directory in ("demo", "evidence"):
        assert (root / directory / f"morning-review-{lang}.md").read_bytes() == expected


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


@pytest.mark.parametrize("lang", ["en", "zh"])
@pytest.mark.parametrize("integration_id", [None, "harbor_android"])
def test_integration_index_resolves_handoff_identity_without_copying_its_values(
    lang, integration_id
):
    workflow = build_demo()
    harbor = next(p for p in workflow["packets"] if p["context"]["account"]["id"] == "acc_006")
    harbor["tickets"][0]["fields"]["app"] = "Different copied handoff value"
    original = copy.deepcopy(workflow)
    brief = render_review_brief(workflow, lang, integration_id)
    index = brief.split("## Integration record index", 1)[1].split(
        "## Product sources and review boundaries", 1
    )[0]
    assert r"| harbor\_android | acc\_006 | Pocket Harbor | Android |" in index
    assert "Different copied handoff value" not in index
    assert "No per-field observation date is recorded" in index
    assert "independently verified" in index
    assert ("Moon Garden" in index) is (integration_id is None)
    assert workflow == original


def test_integration_index_does_not_substitute_missing_ambiguous_or_misscoped_records():
    for fault in ("missing", "duplicate", "other_account", "other_platform"):
        workflow = build_demo()
        packet = next(p for p in workflow["packets"] if p["context"]["account"]["id"] == "acc_006")
        records = packet["context"]["integrations"]
        record = next(i for i in records if i["id"] == "harbor_android")
        record["app"] = "Do not attribute this source"
        if fault == "missing":
            records.remove(record)
        elif fault == "duplicate":
            records.append(copy.deepcopy(record))
        elif fault == "other_account":
            record["account_id"] = "acc_014"
        else:
            record["id"] = "lantern_ios"
        brief = render_review_brief(workflow, integration_id="harbor_android")
        index = brief.split("## Integration record index", 1)[1].split(
            "## Product sources and review boundaries", 1
        )[0]
        assert r"Integration record unavailable or ambiguous: harbor\_android" in index
        assert "Do not attribute this source" not in index


def test_integration_index_keeps_configuration_markup_as_text():
    workflow = build_demo()
    record = workflow["packets"][0]["context"]["integrations"][0]
    record["app"] = "<script>run()</script> | [click](javascript:run())\nFake row"
    brief = render_review_brief(workflow, integration_id=record["id"])
    index = brief.split("## Integration record index", 1)[1]
    assert "<script>" not in index and "[click](javascript:" not in index
    assert r"\| \[click\]" in index
    assert " / Fake row" in index


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
