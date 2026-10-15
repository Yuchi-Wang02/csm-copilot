"""Integrity of published recordings, not a rerun or independent model-quality test."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from csm_copilot.engine import Copilot
from csm_copilot.host_protocol import trace_coverage
from csm_copilot.response_review import review_final

DIRECTORY = Path(__file__).resolve().parents[1] / "evidence/model-runs"


def assert_historical_callback_result(engine, action, recorded):
    current = getattr(engine, action["tool"])(**action["arguments"])
    if action["tool"] == "list_accounts":
        # These two v0.9 recordings predate the additive v0.16.2 time metadata.
        assert action["arguments"] == {"stale_days": 3, "as_of": None, "include_live": False}
        added = {
            "dataset_as_of": recorded["as_of"],
            "time_basis": "dataset_snapshot",
            "records_refreshed": False,
            "time_boundary": (
                "Changing as_of recalculates contact age and time to planned launch from existing "
                "records. It does not refresh contacts, account stages, launch plans or readiness evidence."
            ),
        }
        for key, value in added.items():
            assert key not in recorded
            assert current.pop(key) == value
    if action["tool"] == "draft_ticket":
        # v0.24 adds intake wording without rewriting either v0.9 recording.
        assert action["arguments"] == {"issue_id": "issue_callback"}
        assert "collection_requests" not in recorded and "collection_boundary" not in recorded
        requests = current.pop("collection_requests")
        assert [r["field"] for r in requests] == ["reproduction_steps", "redacted_logs"]
        assert "steps to reproduce" in requests[0]["request"]
        assert "secrets removed" in requests[1]["request"]
        assert "not verified" in current.pop("collection_boundary")
    assert current == recorded


@pytest.mark.parametrize(
    "name",
    [
        "qwen06-single",
        "qwen4-single",
        "qwen4-batch",
        "qwen4-grounded",
        "qwen4-grounded-corrections",
        "qwen4-constrained",
        "qwen4-callback-handoff",
        "qwen4-callback-input-guard",
        "qwen4-triage-scope",
        "qwen4-triage-neutral-questions",
        "qwen4-morning-review",
        "qwen4-morning-sequenced",
        "qwen4-morning-enforced",
        "qwen4-morning-constrained",
    ],
)
def test_recorded_prompt_and_coverage_match_trace(name):
    trace = json.loads((DIRECTORY / f"{name}.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256(
        json.dumps(trace["initial_messages"], ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()
    assert digest == trace["prompt_sha256"]
    assert trace_coverage(trace) == trace["coverage"]
    assert trace["model_inference"] is True
    assert trace["runtime"]["enable_thinking"] is False


def test_morning_recording_preserves_rejected_proposals_without_execution():
    trace = json.loads((DIRECTORY / "qwen4-morning-review.json").read_text(encoding="utf-8"))
    assert trace["task_id"] == "morning_review"
    assert trace["status"] == "invalid_action"
    assert trace["repair_budget"] == 0 and trace["final"] is None
    assert len(trace["steps"]) == 1
    step = trace["steps"][0]
    proposals = json.loads(step["model_response"]["text"])
    assert len(proposals) == 5
    assert proposals[0] == {
        "tool": "list_accounts",
        "arguments": {"stale_days": 3, "include_live": False},
    }
    assert step["parse_error"] == "An action batch must contain 1..4 actions"
    assert not step.get("tool_calls") and "correction_feedback" not in step
    assert step["model_response"]["token_limit_reached"] is False
    engine = Copilot()
    assert proposals[1]["arguments"]["account_id"] not in engine.accounts
    assert proposals[2]["arguments"]["integration_id"] not in engine.integrations
    assert proposals[4]["arguments"]["issue_id"] not in engine.issues
    assert trace["coverage"]["observed"] == 0 and trace["coverage"]["required"] == 7


def test_morning_instruction_pair_preserves_controls_and_failed_execution():
    import runpy

    original = json.loads((DIRECTORY / "qwen4-morning-review.json").read_text(encoding="utf-8"))
    revised = json.loads((DIRECTORY / "qwen4-morning-sequenced.json").read_text(encoding="utf-8"))
    for key in (
        "task",
        "task_id",
        "model_id",
        "revision",
        "protocol_version",
        "max_steps",
        "repair_budget",
        "constrain_final",
        "runtime",
        "coverage",
    ):
        assert original[key] == revised[key], key
    assert revised["sequence_dependencies"] is True
    guidance = runpy.run_path(str(DIRECTORY.parents[1] / "scripts/run_local_host.py"))[
        "DEPENDENCY_GUIDANCE"
    ]
    before, after = original["initial_messages"], revised["initial_messages"]
    assert before[1:] == after[1:]
    assert after[0]["content"].count(guidance) == 1
    assert after[0]["content"].replace("\n" + guidance, "", 1) == before[0]["content"]
    assert len(revised["steps"]) == 1 and revised["final"] is None
    step = revised["steps"][0]
    assert step["parse_error"] == "An action batch must contain 1..4 actions"
    assert not step.get("tool_calls") and "correction_feedback" not in step
    assert step["model_response"]["token_limit_reached"] is False
    proposals = json.loads(step["model_response"]["text"])
    previous = json.loads(original["steps"][0]["model_response"]["text"])
    assert len(proposals) == 5 and proposals[:4] == previous[:4]
    assert proposals[-1]["arguments"]["issue_id"] == "11223"
    assert "11223" not in Copilot().issues


def test_enforced_morning_run_retains_host_input_and_parser_first_rejection():
    from csm_copilot.dependency_policy import MorningReviewPolicy

    original = json.loads((DIRECTORY / "qwen4-morning-review.json").read_text(encoding="utf-8"))
    revised = json.loads((DIRECTORY / "qwen4-morning-enforced.json").read_text(encoding="utf-8"))
    for key in (
        "initial_messages",
        "prompt_sha256",
        "task",
        "task_id",
        "model_id",
        "revision",
        "protocol_version",
        "max_steps",
        "repair_budget",
        "constrain_final",
        "runtime",
        "coverage",
    ):
        assert original[key] == revised[key], key
    assert revised["enforce_dependencies"] is True
    assert revised["sequence_dependencies"] is False
    assert revised["status"] == "invalid_action"
    assert revised["final"] is None and len(revised["steps"]) == 1
    step = revised["steps"][0]
    state = MorningReviewPolicy().snapshot()
    assert step["policy_before"] == revised["dependency_policy"] == state
    message = step["policy_message"]
    assert message["role"] == "user"
    assert json.loads(message["content"][message["content"].index("{") :]) == state
    assert step["parse_error"] == "An action batch must contain 1..4 actions"
    assert "policy_error" not in step and "actions" not in step
    assert not step.get("tool_calls") and "correction_feedback" not in step
    proposals = json.loads(step["model_response"]["text"])
    assert len(proposals) == 5 and proposals[0] == state["pending_actions"][0]
    engine = Copilot()
    assert proposals[1]["arguments"]["account_id"] not in engine.accounts
    assert proposals[2]["arguments"]["integration_id"] not in engine.integrations
    assert proposals[4]["arguments"]["issue_id"] not in engine.issues
    assert step["model_response"]["output_tokens"] == 110
    assert step["model_response"]["token_limit_reached"] is False
    assert (
        step["model_response"]["input_tokens"]
        > original["steps"][0]["model_response"]["input_tokens"]
    )


def test_constrained_morning_recording_preserves_each_schema_scope_and_returned_result():
    from jsonschema import Draft202012Validator

    from csm_copilot.dependency_policy import MorningReviewPolicy

    original = json.loads((DIRECTORY / "qwen4-morning-enforced.json").read_text(encoding="utf-8"))
    trace = json.loads((DIRECTORY / "qwen4-morning-constrained.json").read_text(encoding="utf-8"))
    for key in (
        "initial_messages",
        "task",
        "task_id",
        "model_id",
        "revision",
        "protocol_version",
        "max_steps",
        "repair_budget",
        "constrain_final",
        "runtime",
        "sequence_dependencies",
        "enforce_dependencies",
        "prompt_sha256",
    ):
        assert trace[key] == original[key], key
    assert trace["constrain_actions"] is True
    assert len(trace["steps"]) == 7
    assert trace["coverage"]["observed"] == trace["coverage"]["required"] == 7
    policy, engine = MorningReviewPolicy(), Copilot()
    for step in trace["steps"]:
        assert step["policy_before"] == policy.snapshot()
        assert step["generation_schema"] == policy.next_action_schema()
        assert "choose exactly one pending action" in step["policy_message"]["content"]
        assert step["model_response"]["schema_constrained"] is True
        assert step["model_response"]["token_limit_reached"] is False
        assert "correction_feedback" not in step
        proposal = json.loads(step["model_response"]["text"])
        Draft202012Validator(step["generation_schema"]).validate(proposal)
        assert step["actions"] == [proposal]
        assert len(step["tool_calls"]) == 1
        call = step["tool_calls"][0]
        assert call["action"] == proposal and call["tool_error"] is False
        assert call["tool_result"] == getattr(engine, proposal["tool"])(**proposal["arguments"])
        policy.validate_batch([proposal])
        policy.observe(proposal, call["tool_result"])
        assert call["policy_after"] == policy.snapshot()
    assert trace["dependency_policy"] == policy.snapshot()
    assert policy.stage == "complete" and not policy.pending
    assert trace["final"] is None
    assert trace["status"] == "host_error" and trace["error_type"] == "ExceptionGroup"


def test_constrained_morning_terminal_observation_is_separate_and_trace_bound():
    raw = (DIRECTORY / "qwen4-morning-constrained.json").read_bytes()
    trace = json.loads(raw)
    observation = json.loads(
        (DIRECTORY.parent / "host-observations/qwen4-morning-constrained.json").read_text(
            encoding="utf-8"
        )
    )
    assert observation["trace_sha256"] == hashlib.sha256(raw).hexdigest()
    assert observation["trace_error_type"] == trace["error_type"] == "ExceptionGroup"
    assert observation["exit_code"] == 1
    assert observation["stderr_leaf_error"] == "TimeoutError"
    assert observation["response_timeout_seconds"] == 180
    assert observation["final_response_captured"] is False and trace["final"] is None
    assert observation["observed_tool_calls"] == 7
    assert "eighth-turn request" in observation["boundary"]
    assert "Agent-authored" in observation["boundary"]


def test_published_tool_results_match_except_documented_followup_wording():
    trace = json.loads((DIRECTORY / "qwen4-batch.json").read_text(encoding="utf-8"))
    engine = Copilot()
    calls = [c for step in trace["steps"] for c in step.get("tool_calls", [])]
    assert len(calls) == 4
    methods = {"check_readiness": engine.check_readiness, "draft_followup": engine.draft_followup}
    for call in calls:
        action = call["action"]
        expected = deepcopy(call["tool_result"])
        if (
            action["tool"] == "draft_followup"
            and action["arguments"]["integration_id"] == "lantern_android"
        ):
            # v0.28.3 adds recorded-failure attribution; keep the original AI input frozen.
            assert action["arguments"] == {"integration_id": "lantern_android", "lang": "en"}
            old_line = (
                "- Share a fresh non-test-device check with region, time and observed result."
            )
            assert expected["body"].splitlines().count(old_line) == 1
            assert "Our records show this check was not met." not in expected["body"]
            expected["body"] = expected["body"].replace(
                old_line,
                "- Our records show this check was not met. " + old_line[2:],
            )
            expected["draft_id"] = (
                "followup-" + hashlib.sha256(expected["body"].encode()).hexdigest()[:12]
            )
        assert methods[action["tool"]](**action["arguments"]) == expected
    assert trace["final"]  # Prose is separately reviewed, not approved by this test.


def test_inbound_scope_recording_preserves_inputs_routes_and_unedited_prose():
    from csm_copilot.host_protocol import TRIAGE_SCOPE_MESSAGES

    trace = json.loads((DIRECTORY / "qwen4-triage-scope.json").read_text(encoding="utf-8"))
    assert trace["task_id"] == "triage_scope"
    assert trace["project_version"] == "0.11.0"
    assert trace["coverage"]["observed"] == trace["coverage"]["required"] == 2
    assert trace["repair_budget"] == 0
    calls = [c for s in trace["steps"] for c in s.get("tool_calls", [])]
    assert len(calls) == 2
    assert [c["action"]["arguments"]["issue_text"] for c in calls] == list(
        TRIAGE_SCOPE_MESSAGES.values()
    )
    engine = Copilot()
    for call in calls:
        assert call["action"]["tool"] == "triage_issue"
        assert call["action"]["arguments"]["integration_id"] is None
        assert not call["tool_error"]
        expected = deepcopy(call["tool_result"])
        if expected["candidates"][0]["category"] == "unknown":
            assert expected["candidates"][0]["questions"] == [
                "What happened, what was expected, and which app/platform is affected?"
            ]
            expected["candidates"][0]["questions"] = [
                "Which account or product does this request concern?",
                "What specific information or outcome do you need, and which relevant details should we review?",
            ]
        assert expected == engine.triage_issue(**call["action"]["arguments"])
    assert [c["tool_result"]["route"] for c in calls] == ["clarify_scope", "collect_evidence"]
    assert not any("correction_feedback" in s for s in trace["steps"])
    assert json.loads(trace["steps"][-1]["model_response"]["text"])["final"] == trace["final"]


def test_neutral_question_pair_preserves_controls_and_limits_the_tool_result_change():
    before = json.loads((DIRECTORY / "qwen4-triage-scope.json").read_text(encoding="utf-8"))
    after = json.loads(
        (DIRECTORY / "qwen4-triage-neutral-questions.json").read_text(encoding="utf-8")
    )
    assert after["project_version"] == "0.11.1"
    for key in (
        "task",
        "task_id",
        "initial_messages",
        "prompt_sha256",
        "runtime",
        "model_id",
        "revision",
    ):
        assert before[key] == after[key]
    assert before["steps"][0]["actions"] == after["steps"][0]["actions"]
    old_calls = [c for s in before["steps"] for c in s.get("tool_calls", [])]
    new_calls = [c for s in after["steps"] for c in s.get("tool_calls", [])]
    assert len(old_calls) == len(new_calls) == 2
    assert after["coverage"]["observed"] == after["coverage"]["required"] == 2
    engine = Copilot()
    for old, new in zip(old_calls, new_calls, strict=True):
        assert old["action"] == new["action"]
        assert not new["tool_error"]
        assert new["tool_result"] == engine.triage_issue(**new["action"]["arguments"])
        expected = deepcopy(old["tool_result"])
        if expected["candidates"][0]["category"] == "unknown":
            assert (
                expected["candidates"][0]["questions"]
                != new["tool_result"]["candidates"][0]["questions"]
            )
            expected["candidates"][0]["questions"] = new["tool_result"]["candidates"][0][
                "questions"
            ]
        assert expected == new["tool_result"]
    assert after["repair_budget"] == 0
    assert not any("correction_feedback" in step for step in after["steps"])
    assert json.loads(after["steps"][-1]["model_response"]["text"])["final"] == after["final"]


def test_recorded_corrections_and_field_reviews_are_reproducible():
    trace = json.loads((DIRECTORY / "qwen4-constrained.json").read_text(encoding="utf-8"))
    corrections = [s for s in trace["steps"] if "correction_feedback" in s]
    assert len(corrections) == 2
    assert [s["repair_number"] for s in corrections] == [1, 2]
    for index, step in enumerate(trace["steps"]):
        if "response_review" in step:
            prefix = {**trace, "steps": trace["steps"][: index + 1]}
            final = step["actions"][0]["final"]
            assert review_final(final, prefix) == step["response_review"]
            assert step["model_response"]["schema_constrained"] is True
    assert trace["status"] == "structured_fields_match"
    assert review_final(trace["final"], trace) == trace["response_review"]
    assert trace["response_review"]["free_text_verification"] == "not_performed"


def test_callback_handoff_preserves_the_historical_identifier_input_error():
    trace = json.loads((DIRECTORY / "qwen4-callback-handoff.json").read_text(encoding="utf-8"))
    assert trace["task_id"] == "callback_handoff"
    assert trace["coverage"]["observed"] == trace["coverage"]["required"] == 2
    engine = Copilot()
    calls = [c for step in trace["steps"] for c in step.get("tool_calls", [])]
    assert len(calls) == 4
    for call in calls:
        action = call["action"]
        if action["tool"] == "triage_issue":
            # The v0.9 recording is immutable. v0.9.1 rejects this formerly accepted input.
            assert action["arguments"]["issue_text"] == "issue_callback"
            assert call["tool_error"] is False
            assert call["tool_result"]["candidates"][0]["category"] == "reward_callback"
            with pytest.raises(ValueError, match="customer message, not a recorded issue ID"):
                engine.triage_issue(**action["arguments"])
            continue
        assert_historical_callback_result(engine, action, call["tool_result"])
    assert not any("correction_feedback" in step for step in trace["steps"])


def test_identifier_check_recording_preserves_the_tool_error_and_successful_handoff():
    trace = json.loads((DIRECTORY / "qwen4-callback-input-guard.json").read_text(encoding="utf-8"))
    previous = json.loads((DIRECTORY / "qwen4-callback-handoff.json").read_text(encoding="utf-8"))
    assert trace["project_version"] == "0.9.1"
    assert trace["steps"][0]["actions"] == previous["steps"][0]["actions"]
    assert trace["coverage"]["observed"] == trace["coverage"]["required"] == 2
    calls = [c for s in trace["steps"] for c in s.get("tool_calls", [])]
    assert len(calls) == 4
    assert sum(c["tool_error"] for c in calls) == 1
    engine = Copilot()
    for call in calls:
        action = call["action"]
        if call["tool_error"]:
            assert action["tool"] == "triage_issue"
            assert "customer message, not a recorded issue ID" in call["tool_result"][0]["text"]
            with pytest.raises(ValueError, match="customer message, not a recorded issue ID"):
                engine.triage_issue(**action["arguments"])
        else:
            assert_historical_callback_result(engine, action, call["tool_result"])
    assert not any("correction_feedback" in step for step in trace["steps"])
