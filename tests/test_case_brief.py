"""A selected-platform export must not borrow another platform's evidence or handoff."""

import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from csm_copilot.brief import render_review_brief, text
from csm_copilot.demo import build_demo

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "integration_id", ["lantern_android", "lantern_ios", "meadow_ios", "harbor_android"]
)
@pytest.mark.parametrize("lang", ["en", "zh"])
def test_export_keeps_only_selected_platform_and_account_contact_evidence(integration_id, lang):
    workflow = build_demo()
    original = deepcopy(workflow)
    brief = render_review_brief(workflow, lang, integration_id)
    packet = next(
        p for p in workflow["packets"] if integration_id in p["selection"]["integration_ids"]
    )
    account_id = packet["context"]["account"]["id"]
    assert "Platform review brief" in brief
    assert "Original snapshot only" in brief
    assert "Nothing was sent or submitted" in brief
    assert "reply\\_android\\_settings" not in brief
    for p in workflow["packets"]:
        for record in p["context"]["evidence"]:
            belongs = record["account_id"] == account_id and record["integration_id"] in (
                None,
                integration_id,
            )
            assert (f"| {text(record['id'])} |" in brief) is belongs
        for issue in p["context"]["issues"]:
            assert (text(f"ticket-{issue['id']}") in brief) is (
                issue["integration_id"] == integration_id
            )
    assert workflow == original
    assert (ROOT / f"demo/case-briefs/{integration_id}-{lang}.md").read_bytes() == brief.encode("utf-8")


def test_ios_brief_has_no_android_failure_or_handoff_and_preserves_launch_plan():
    brief = render_review_brief(build_demo(), "zh", "lantern_ios")
    assert "### Moon Garden / iOS" in brief
    assert "Review the launch plan" in brief
    assert "Lantern Games 团队好" in brief
    assert "**Recorded issues:** None for this platform" in brief
    assert "lantern\\_android" not in brief
    assert "Technical handoff" not in brief


def test_every_issue_on_the_selected_platform_keeps_its_handoff():
    workflow = build_demo()
    packet = workflow["packets"][0]
    issue = deepcopy(packet["context"]["issues"][0])
    issue["id"] = "issue_second"
    packet["context"]["issues"].append(issue)
    ticket = deepcopy(packet["tickets"][0])
    ticket["draft_id"] = "ticket-issue_second"
    packet["tickets"].append(ticket)
    brief = render_review_brief(workflow, integration_id="lantern_android")
    assert "ticket-issue\\_blank" in brief and "ticket-issue\\_second" in brief
    assert brief.count("### Technical handoff") == 2


@pytest.mark.parametrize("identifier", ["missing", "orbit_android", "", "../lantern_android"])
def test_unknown_or_unqueued_platform_is_not_replaced_with_another_case(identifier):
    with pytest.raises(ValueError, match="exactly one platform"):
        render_review_brief(build_demo(), integration_id=identifier)


def test_duplicate_platform_is_rejected_instead_of_choosing_first():
    workflow = build_demo()
    workflow["packets"].append(deepcopy(workflow["packets"][0]))
    with pytest.raises(ValueError, match="exactly one platform"):
        render_review_brief(workflow, integration_id="lantern_android")


@pytest.mark.parametrize(
    "arguments",
    [["--integration", "lantern_ios"], ["--format", "markdown", "--integration", "missing"]],
)
def test_cli_rejects_ambiguous_format_or_unknown_scope_before_writing(tmp_path, arguments):
    target = tmp_path / "preserved.md"
    target.write_text("existing brief", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "csm_copilot.demo", *arguments, "--output", str(target)],
        capture_output=True,
        timeout=20,
    )
    assert result.returncode == 2
    assert b"Traceback" not in result.stderr
    assert target.read_text(encoding="utf-8") == "existing brief"


def test_download_directory_has_exactly_the_queued_platforms_in_both_languages():
    expected = {
        f"{i['readiness']['integration_id']}-{lang}.md"
        for p in build_demo()["packets"]
        for i in p["integrations"]
        for lang in ("en", "zh")
    }
    assert {p.name for p in (ROOT / "demo/case-briefs").glob("*.md")} == expected
