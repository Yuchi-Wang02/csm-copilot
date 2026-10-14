"""Request missing structured intake fields without treating presence as verification."""

from copy import deepcopy

import pytest

from csm_copilot.brief import render_review_brief
from csm_copilot.demo import build_demo
from csm_copilot.engine import Copilot


def test_harbor_requests_only_missing_steps_and_logs_and_preserves_known_sources():
    engine = Copilot()
    before = engine.data.model_dump()
    ticket = engine.draft_ticket("issue_callback")
    assert [r["field"] for r in ticket["collection_requests"]] == [
        "reproduction_steps",
        "redacted_logs",
    ]
    assert "expected" in ticket["collection_requests"][0]["request"]
    assert "secrets" in ticket["collection_requests"][1]["request"]
    assert ticket["field_sources"]["time_window"]["source_id"] == "msg_issue_callback"
    assert ticket["root_cause"] == "unconfirmed" and ticket["sent"] is False
    assert engine.data.model_dump() == before


@pytest.mark.parametrize("complete", [False, True])
def test_unknown_scope_never_requests_generic_technical_fields(complete):
    data = Copilot().data.model_copy(deep=True)
    issue = next(i for i in data.issues if i.id == "issue_callback")
    issue.summary = "Please explain invoicing."
    if complete:
        for field in type(issue.details).model_fields:
            setattr(issue.details, field, "Recorded placeholder")
    ticket = Copilot(data).draft_ticket(issue.id)
    assert ticket["collection_requests"] == []
    assert ticket["handoff_state"] == "needs_scope"


def test_all_fields_present_requires_review_without_a_redundant_request():
    data = Copilot().data.model_copy(deep=True)
    issue = next(i for i in data.issues if i.id == "issue_callback")
    issue.details.reproduction_steps = "Placeholder; not yet reviewed."
    issue.details.redacted_logs = "Placeholder; not yet reviewed."
    ticket = Copilot(data).draft_ticket(issue.id)
    assert ticket["collection_requests"] == []
    assert ticket["handoff_state"] == "ready_for_human_review"
    assert "not verified" in ticket["collection_boundary"]
    assert ticket["root_cause"] == "unconfirmed"


def test_whitespace_field_is_requested_even_when_the_original_message_mentions_it():
    data = Copilot().data.model_copy(deep=True)
    issue = next(i for i in data.issues if i.id == "issue_callback")
    issue.details.time_window = "  "
    ticket = Copilot(data).draft_ticket(issue.id)
    assert "time_window" in [r["field"] for r in ticket["collection_requests"]]
    assert "08:30" in ticket["customer_report"]
    assert "structured" in ticket["collection_boundary"]


def test_request_lists_are_independent_and_do_not_borrow_other_issue_fields():
    engine = Copilot()
    ticket = engine.draft_ticket("issue_blank")
    expected = deepcopy(ticket["collection_requests"])
    assert "sdk_version" in [r["field"] for r in expected]
    assert "sdk_version" not in [
        r["field"] for r in engine.draft_ticket("issue_callback")["collection_requests"]
    ]
    ticket["collection_requests"][0]["request"] = "Modified caller copy"
    assert engine.draft_ticket("issue_blank")["collection_requests"] == expected


def test_export_keeps_focused_request_separate_from_broader_triage_questions():
    workflow = build_demo()
    brief = render_review_brief(workflow, integration_id="harbor_android")
    focused = brief.split("**Request missing intake details**", 1)[1].split(
        "**Original issue record**", 1
    )[0]
    assert "steps to reproduce" in focused and "secrets removed" in focused
    assert "Share the SDK version" not in focused
    assert "Share the observation start" not in focused
    assert "not verified" in focused
    assert "Share the callback time window" in brief
