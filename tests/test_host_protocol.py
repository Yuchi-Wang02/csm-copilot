import pytest

from csm_copilot.host_protocol import parse_action, parse_actions, trace_coverage


@pytest.mark.parametrize(
    "raw",
    [
        '```json\n{"tool":"check_readiness","arguments":{}}\n```',
        '{"tool":"shell","arguments":{"command":"whoami"}}',
        '{"tool":"check_readiness","arguments":{},"final":"done"}',
        '{"tool":"check_readiness","arguments":[]}',
        '{"tool":[],"arguments":{}}',
        '{"tool":"check_readiness","tool":"shell","arguments":{}}',
        '{"tool":"check_readiness","arguments":{"x":NaN}}',
        '[{"tool":"check_readiness","arguments":{}}]',
        '{"final":""}',
    ],
)
def test_invalid_actions_never_become_tool_requests(raw):
    with pytest.raises(ValueError):
        parse_action(raw, {"check_readiness"})


def test_valid_action_and_final_are_preserved_without_repair():
    raw = '{"tool":"check_readiness","arguments":{"integration_id":"lantern_android"}}'
    assert (
        parse_action(raw, {"check_readiness"})["arguments"]["integration_id"] == "lantern_android"
    )
    assert parse_action('{"final":"Nothing was sent."}', set()) == {"final": "Nothing was sent."}


@pytest.mark.parametrize(
    "raw",
    [
        "[]",
        '[{"tool":"check_readiness","arguments":{}},{"tool":"shell","arguments":{}}]',
        '[{"tool":"check_readiness","arguments":{}},{"final":"done"}]',
        '{"tool":"check_readiness","arguments":{}}\n{"tool":"check_readiness","arguments":{}}',
    ],
)
def test_invalid_batches_are_rejected_as_a_whole(raw):
    with pytest.raises(ValueError):
        parse_actions(raw, {"check_readiness"})


def test_explicit_batch_preserves_model_chosen_order():
    raw = '[{"tool":"check_readiness","arguments":{"integration_id":"a"}},{"tool":"check_readiness","arguments":{"integration_id":"b"}}]'
    assert [a["arguments"]["integration_id"] for a in parse_actions(raw, {"check_readiness"})] == [
        "a",
        "b",
    ]


def test_final_text_does_not_substitute_for_required_tool_evidence():
    result = trace_coverage({"steps": [], "final": "I checked both integrations."})
    assert result["observed"] == 0
    assert result["final_response_present"] is True


def test_handoff_coverage_requires_its_own_account_and_issue_calls():
    calls = [
        {
            "action": {"tool": "get_account_context", "arguments": {"account_id": "acc_006"}},
            "tool_result": {},
        },
        {
            "action": {"tool": "draft_ticket", "arguments": {"issue_id": "issue_blank"}},
            "tool_result": {},
        },
        {
            "action": {"tool": "draft_ticket", "arguments": {"issue_id": "issue_callback"}},
            "tool_result": {},
            "tool_error": True,
        },
    ]
    trace = {"task_id": "callback_handoff", "steps": [{"tool_calls": calls}]}
    assert trace_coverage(trace)["observed"] == 1
    assert trace_coverage(trace)["required"] == 2
    calls[-1]["tool_error"] = False
    assert trace_coverage(trace)["observed"] == 2
    trace["task_id"] = "platform_followups"
    assert trace_coverage(trace)["observed"] == 0


def test_unknown_recorded_task_cannot_silently_use_default_coverage():
    with pytest.raises(ValueError, match="Unknown recorded task"):
        trace_coverage({"task_id": "invented_task", "steps": []})


def test_inbound_triage_coverage_preserves_the_two_messages_and_unknown_identity():
    from csm_copilot.host_protocol import TRIAGE_SCOPE_MESSAGES

    calls = [
        {
            "action": {"tool": "triage_issue", "arguments": {"issue_text": message}},
            "tool_result": {},
        }
        for message in TRIAGE_SCOPE_MESSAGES.values()
    ]
    trace = {"task_id": "triage_scope", "steps": [{"tool_calls": calls}]}
    assert trace_coverage(trace)["observed"] == trace_coverage(trace)["required"] == 2
    calls[0]["action"]["arguments"]["integration_id"] = "lantern_android"
    assert trace_coverage(trace)["observed"] == 1
    calls[0]["action"]["arguments"]["integration_id"] = None
    calls[1]["action"]["arguments"]["issue_text"] = TRIAGE_SCOPE_MESSAGES["invoice_request"]
    assert trace_coverage(trace)["observed"] == 1
    calls[0]["tool_error"] = True
    calls[1]["tool_error"] = True
    assert trace_coverage(trace)["observed"] == 0


def test_failed_calls_and_wrong_language_do_not_satisfy_coverage():
    trace = {
        "steps": [
            {
                "action": {
                    "tool": "check_readiness",
                    "arguments": {"integration_id": "lantern_android"},
                },
                "tool_result": {},
                "tool_error": True,
            },
            {
                "action": {
                    "tool": "draft_followup",
                    "arguments": {"integration_id": "lantern_android", "lang": "zh"},
                },
                "tool_result": {},
                "tool_error": False,
            },
            {
                "action": {
                    "tool": "check_readiness",
                    "arguments": {"integration_id": "lantern_ios"},
                },
                "tool_result": {},
                "tool_error": False,
            },
        ]
    }
    result = trace_coverage(trace)
    assert result["observed"] == 1
    assert result["checks"]["ios_readiness"] is True
