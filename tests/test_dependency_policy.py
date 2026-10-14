"""Dependency boundaries use unfamiliar IDs, not the demonstration's known answers."""

from copy import deepcopy

import pytest

from csm_copilot.dependency_policy import DependencyPolicyError, MorningReviewPolicy, action

QUEUE = action("list_accounts")
CONTEXT = action("get_account_context", account_id="new-account")
QUEUE_RESULT = {
    "accounts": [{"account_id": "new-account"}, {"account_id": "other-account"}],
    "time_basis": "dataset_snapshot",
    "stale_days": 3,
}
CONTEXT_RESULT = {
    "account": {"id": "new-account"},
    "integrations": [{"id": "new-platform", "account_id": "new-account"}],
    "issues": [{"id": "new-issue", "integration_id": "new-platform"}],
}


def review_policy():
    policy = MorningReviewPolicy()
    policy.observe(QUEUE, QUEUE_RESULT)
    policy.observe(CONTEXT, CONTEXT_RESULT)
    return policy


@pytest.mark.parametrize(
    "batch",
    [
        [QUEUE, CONTEXT],
        [QUEUE, QUEUE],
        [CONTEXT],
        [{"final": "Done"}],
        [action("list_accounts", stale_days=4)],
        [action("list_accounts", include_live=True)],
        [action("list_accounts", include_live=0)],
        [action("list_accounts", as_of="2026-10-17T09:00:00Z")],
        [action("list_accounts", extra="ignored?")],
        [action("triage_issue", issue_text="blank")],
    ],
)
def test_invalid_initial_batch_preserves_all_state(batch):
    policy = MorningReviewPolicy()
    before = policy.snapshot()
    with pytest.raises(DependencyPolicyError):
        policy.validate_batch(batch)
    assert policy.snapshot() == before


def test_proposals_and_error_results_do_not_unlock_context():
    policy = MorningReviewPolicy()
    policy.validate_batch([QUEUE])
    policy.observe(QUEUE, {"error": "not ready"}, tool_error=True)
    assert policy.stage == "awaiting_queue"
    assert policy.completed == []
    with pytest.raises(DependencyPolicyError):
        policy.validate_batch([CONTEXT])


def test_context_must_use_first_successfully_returned_account():
    policy = MorningReviewPolicy()
    policy.observe(QUEUE, QUEUE_RESULT)
    assert policy.account_id == "new-account"
    with pytest.raises(DependencyPolicyError):
        policy.validate_batch([action("get_account_context", account_id="other-account")])
    with pytest.raises(DependencyPolicyError):
        policy.validate_batch([CONTEXT, action("check_readiness", integration_id="new-platform")])
    policy.validate_batch([CONTEXT])


@pytest.mark.parametrize(
    "proposal",
    [
        action("check_readiness", integration_id="lantern_android"),
        action("draft_ticket", issue_id="issue_blank"),
        action("draft_followup", integration_id="new-platform", lang="zh"),
        action("get_account_context", account_id="new-account"),
        {"final": "Everything is done"},
    ],
)
def test_review_rejects_unknown_ids_wrong_language_and_premature_final(proposal):
    policy = review_policy()
    with pytest.raises(DependencyPolicyError):
        policy.validate_batch([proposal])


@pytest.mark.parametrize(
    "result",
    [
        {},
        {**QUEUE_RESULT, "accounts": [{}]},
        {**QUEUE_RESULT, "accounts": [{"account_id": "a"}, {"account_id": "a"}]},
        {**QUEUE_RESULT, "time_basis": "recalculated_from_snapshot"},
        {**QUEUE_RESULT, "stale_days": 2},
        [],
    ],
)
def test_malformed_queue_results_never_advance(result):
    policy = MorningReviewPolicy()
    before = policy.snapshot()
    with pytest.raises(DependencyPolicyError):
        policy.observe(QUEUE, result)
    assert policy.snapshot() == before


@pytest.mark.parametrize(
    "field,value",
    [
        ("account", {"id": "wrong-account"}),
        ("integrations", [{"id": "new-platform", "account_id": "wrong-account"}]),
        ("issues", [{"id": "new-issue", "integration_id": "wrong-platform"}]),
        ("issues", [{"id": "duplicate"}, {"id": "duplicate"}]),
        ("integrations", None),
    ],
)
def test_context_scope_or_shape_errors_leave_context_pending(field, value):
    policy = MorningReviewPolicy()
    policy.observe(QUEUE, QUEUE_RESULT)
    before = policy.snapshot()
    with pytest.raises(DependencyPolicyError):
        policy.observe(CONTEXT, {**CONTEXT_RESULT, field: value})
    assert policy.snapshot() == before


def test_all_successful_work_required_and_duplicates_do_not_count():
    policy = review_policy()
    readiness = action("check_readiness", integration_id="new-platform")
    followup = action("draft_followup", integration_id="new-platform")
    ticket = action("draft_ticket", issue_id="new-issue")
    batch = [readiness, followup, ticket]
    before = policy.snapshot()
    policy.validate_batch(batch)
    assert policy.snapshot() == before
    policy.observe(
        readiness, {"integration_id": "new-platform", "decision": "blocked", "checks": []}
    )
    with pytest.raises(DependencyPolicyError):
        policy.validate_batch([readiness])
    policy.observe(followup, {"state": "draft", "sent": False, "lang": "en", "body": "Hello"})
    policy.observe(ticket, {}, tool_error=True)
    with pytest.raises(DependencyPolicyError):
        policy.validate_batch([{"final": "Done"}])
    policy.observe(
        ticket,
        {
            "state": "draft",
            "sent": False,
            "draft_id": "ticket-new-issue",
            "fields": {},
            "missing_fields": ["logs"],
        },
    )
    policy.validate_batch([{"final": "Needs logs; nothing sent."}])
    assert policy.stage == "complete"
    assert len(policy.completed) == 5


@pytest.mark.parametrize(
    "proposal,result",
    [
        (
            action("check_readiness", integration_id="new-platform"),
            {"integration_id": "other", "decision": "blocked", "checks": []},
        ),
        (action("check_readiness", integration_id="new-platform"), {}),
        (
            action("draft_followup", integration_id="new-platform"),
            {"state": "draft", "sent": False, "lang": "zh", "body": "Hello"},
        ),
        (
            action("draft_followup", integration_id="new-platform"),
            {"state": "draft", "sent": False, "lang": "en", "body": " "},
        ),
        (action("draft_ticket", issue_id="new-issue"), {"state": "draft", "sent": True}),
        (
            action("draft_ticket", issue_id="new-issue"),
            {
                "state": "draft",
                "sent": False,
                "draft_id": "ticket-other",
                "fields": {},
                "missing_fields": [],
            },
        ),
    ],
)
def test_malformed_or_mismatched_work_results_do_not_count(proposal, result):
    policy = review_policy()
    before = policy.snapshot()
    with pytest.raises(DependencyPolicyError):
        policy.observe(proposal, result)
    assert policy.snapshot() == before


def test_empty_queue_and_empty_account_have_explicit_completion_paths():
    policy = MorningReviewPolicy()
    policy.observe(QUEUE, {**QUEUE_RESULT, "accounts": []})
    policy.validate_batch([{"final": "Queue empty."}])
    assert policy.account_id is None
    assert len(policy.completed) == 1
    policy = MorningReviewPolicy()
    policy.observe(QUEUE, QUEUE_RESULT)
    policy.observe(CONTEXT, {**CONTEXT_RESULT, "integrations": [], "issues": []})
    policy.validate_batch([{"final": "No integration or issue records to review."}])
    assert len(policy.completed) == 2


def test_snapshot_cannot_modify_live_policy():
    policy = review_policy()
    original = deepcopy(policy.snapshot())
    exposed = policy.snapshot()
    exposed["pending_actions"].clear()
    exposed["completed_actions"][0]["arguments"]["stale_days"] = 999
    assert policy.snapshot() == original
