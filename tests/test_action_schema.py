"""Check schema meaning and actual decoder acceptance without loading model weights."""

import json
from copy import deepcopy

import pytest
from jsonschema import Draft202012Validator
from lmformatenforcer import JsonSchemaParser

from csm_copilot.dependency_policy import MorningReviewPolicy, action
from csm_copilot.engine import Copilot


def decoder_accepts(schema, value):
    parser = JsonSchemaParser(schema)
    for character in json.dumps(value, ensure_ascii=False):
        if character not in parser.get_allowed_characters():
            return False
        parser = parser.add_character(character)
    return parser.can_end()


def assert_contract(schema, value, accepted):
    Draft202012Validator.check_schema(schema)
    assert Draft202012Validator(schema).is_valid(value) is accepted
    assert decoder_accepts(schema, value) is accepted


def reviewing_policy():
    policy = MorningReviewPolicy()
    policy.observe(
        action("list_accounts"),
        {
            "accounts": [{"account_id": "fresh-account"}],
            "time_basis": "dataset_snapshot",
            "stale_days": 3,
        },
    )
    policy.observe(
        action("get_account_context", account_id="fresh-account"),
        {
            "account": {"id": "fresh-account"},
            "integrations": [
                {"id": "first-platform", "account_id": "fresh-account"},
                {"id": "second-platform", "account_id": "fresh-account"},
            ],
            "issues": [{"id": "fresh-issue", "integration_id": "first-platform"}],
        },
    )
    return policy


@pytest.mark.parametrize(
    "value,accepted",
    [
        (action("list_accounts"), True),
        ([action("list_accounts")], False),
        ([action("list_accounts")] * 5, False),
        (action("get_account_context", account_id="12345"), False),
        ({"final": "Done"}, False),
        (action("list_accounts", stale_days=3), False),
        (action("list_accounts", include_live=True), False),
        ({"tool": "list_accounts", "arguments": {}, "extra": "text"}, False),
        ({"tool": "list_accounts"}, False),
    ],
)
def test_initial_decoder_allows_only_one_default_queue_object(value, accepted):
    assert_contract(MorningReviewPolicy().next_action_schema(), value, accepted)


def test_context_schema_uses_the_returned_account_only():
    policy = MorningReviewPolicy()
    policy.observe(
        action("list_accounts"),
        {
            "accounts": [{"account_id": "fresh-account"}],
            "time_basis": "dataset_snapshot",
            "stale_days": 3,
        },
    )
    schema = policy.next_action_schema()
    assert_contract(schema, action("get_account_context", account_id="fresh-account"), True)
    assert_contract(schema, action("get_account_context", account_id="12345"), False)
    assert_contract(schema, action("check_readiness", integration_id="first-platform"), False)


def test_review_schema_preserves_tool_and_argument_pairing_and_completed_work():
    policy = reviewing_policy()
    schema = policy.next_action_schema()
    before = policy.snapshot()
    for pending in policy.pending:
        assert_contract(schema, pending, True)
    assert policy.snapshot() == before
    for invalid in (
        action("draft_ticket", integration_id="first-platform"),
        action("draft_ticket", issue_id="first-platform"),
        action("draft_followup", integration_id="first-platform", lang="zh"),
        action("check_readiness", integration_id="foreign-platform"),
        action("get_account_context", account_id="fresh-account"),
        [policy.pending[0], policy.pending[1]],
        {"final": "Done"},
    ):
        assert_contract(schema, invalid, False)
    completed = deepcopy(policy.pending[0])
    policy.observe(
        completed,
        {
            "integration_id": "first-platform",
            "decision": "blocked",
            "checks": [],
        },
    )
    assert_contract(policy.next_action_schema(), completed, False)
    policy.observe(policy.pending[0], {}, tool_error=True)
    assert_contract(policy.next_action_schema(), policy.pending[0], True)


def test_real_fixture_can_complete_with_seven_single_calls_and_a_final():
    engine, policy = Copilot(), MorningReviewPolicy()
    count = 0
    while policy.pending:
        schema = policy.next_action_schema()
        proposal = deepcopy(policy.pending[-1])
        if proposal["tool"] == "list_accounts":
            proposal["arguments"] = {}
        assert_contract(schema, proposal, True)
        policy.validate_batch([proposal])
        result = getattr(engine, proposal["tool"])(**proposal["arguments"])
        policy.observe(proposal, result)
        count += 1
        assert count <= 7
    assert count == 7
    assert_contract(policy.next_action_schema(), {"final": "Nothing was sent."}, True)
    assert_contract(policy.next_action_schema(), action("list_accounts"), False)


def test_final_schema_does_not_certify_the_truth_of_prose():
    policy = MorningReviewPolicy()
    policy.observe(
        action("list_accounts"),
        {
            "accounts": [],
            "time_basis": "dataset_snapshot",
            "stale_days": 3,
        },
    )
    schema = policy.next_action_schema()
    assert_contract(schema, {"final": "All launches are approved."}, True)
    assert_contract(schema, {"final": ""}, False)
    assert_contract(schema, {"final": {"answer": "Done"}}, False)
    assert_contract(schema, {"final": "Done", "extra": True}, False)


def test_schema_is_a_separate_value_not_a_mutable_policy_reference():
    policy = reviewing_policy()
    before = policy.snapshot()
    schema = policy.next_action_schema()
    schema["anyOf"][0]["properties"]["arguments"]["properties"].clear()
    assert policy.snapshot() == before
    assert_contract(policy.next_action_schema(), policy.pending[0], True)
