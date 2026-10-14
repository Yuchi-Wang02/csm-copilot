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


def test_morning_coverage_requires_queue_selected_context_platforms_and_issue():
    calls = [
        {"action": {"tool": tool, "arguments": arguments}, "tool_result": {}}
        for tool, arguments in [
            ("list_accounts", {}),
            ("get_account_context", {"account_id": "acc_014"}),
            ("check_readiness", {"integration_id": "lantern_android"}),
            ("check_readiness", {"integration_id": "lantern_ios"}),
            ("draft_followup", {"integration_id": "lantern_android"}),
            ("draft_followup", {"integration_id": "lantern_ios", "lang": "en"}),
            ("draft_ticket", {"issue_id": "issue_blank"}),
        ]
    ]
    trace = {"task_id": "morning_review", "steps": [{"tool_calls": calls}]}
    assert trace_coverage(trace)["observed"] == trace_coverage(trace)["required"] == 7
    calls[0]["action"]["arguments"] = {"stale_days": 1}
    calls[1]["action"]["arguments"]["account_id"] = "acc_006"
    calls[-1]["action"]["arguments"]["issue_id"] = "issue_callback"
    assert trace_coverage(trace)["observed"] == 4
    calls[0]["action"]["arguments"] = {"stale_days": 3, "as_of": None, "include_live": False}
    assert trace_coverage(trace)["checks"]["morning_queue"] is True
    for call in calls:
        call["tool_error"] = True
    trace["final"] = "All work completed."
    assert trace_coverage(trace)["observed"] == 0


@pytest.mark.parametrize("arguments", [{"include_live": True}, {"as_of": "2026-10-17"}])
def test_morning_coverage_does_not_credit_a_different_queue(arguments):
    trace = {
        "task_id": "morning_review",
        "steps": [
            {
                "tool_calls": [
                    {"action": {"tool": "list_accounts", "arguments": arguments}, "tool_result": {}}
                ]
            }
        ],
    }
    assert trace_coverage(trace)["observed"] == 0


def test_morning_expectations_match_the_actual_fixed_queue_without_prompt_identifiers():
    import runpy
    from pathlib import Path

    from csm_copilot.engine import Copilot

    engine = Copilot()
    queue = engine.list_accounts()
    first = queue["accounts"][0]
    assert first["account_id"] == "acc_014"
    context = engine.get_account_context(first["account_id"])
    assert {i["id"] for i in context["integrations"]} == {"lantern_android", "lantern_ios"}
    assert {i["id"] for i in context["issues"]} == {"issue_blank"}
    task = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/run_local_host.py"))[
        "TASKS"
    ]["morning_review"]
    for identifier in ("acc_014", "lantern_android", "lantern_ios", "issue_blank", "Lantern"):
        assert identifier not in task


def test_dependency_guidance_is_explicit_and_does_not_change_default_prompts():
    import runpy
    from pathlib import Path

    host = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/run_local_host.py"))
    for protocol, name in [
        ("single", "SINGLE_SYSTEM"),
        ("batch", "SYSTEM"),
        ("grounded", "GROUNDED_SYSTEM"),
    ]:
        assert host["system_prompt"](protocol) == host[name]
    guided = host["system_prompt"]("batch", True)
    assert guided.replace("\n" + host["DEPENDENCY_GUIDANCE"], "", 1) == host["SYSTEM"]
    assert guided.count(host["DEPENDENCY_GUIDANCE"]) == 1
    assert guided.endswith("\nAvailable tools:\n")
    for identifier in (
        "acc_014",
        "lantern_android",
        "lantern_ios",
        "issue_blank",
        "12345",
        "67890",
    ):
        assert identifier not in guided
