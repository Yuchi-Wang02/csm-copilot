"""Audit recorded correction provenance; no inference or independent prose assessment."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from csm_copilot.dependency_policy import MorningReviewPolicy
from csm_copilot.engine import Copilot
from csm_copilot.host_context import compact_final_messages
from csm_copilot.morning_review import (
    MORNING_EXPLANATION_GUIDANCE,
    MORNING_FINAL_GUIDANCE,
    review_morning_final,
)

DIRECTORY = Path(__file__).resolve().parents[1] / "evidence/model-runs"


def test_correction_attempt_reproduces_the_prior_eight_requests_before_feedback():
    prior = json.loads(
        (DIRECTORY / "qwen4-morning-compact-context.json").read_text(encoding="utf-8")
    )
    trace = json.loads((DIRECTORY / "qwen4-morning-correction.json").read_text(encoding="utf-8"))
    for key in (
        "runtime",
        "task",
        "task_id",
        "model_id",
        "revision",
        "initial_messages",
        "protocol_version",
        "response_timeout_seconds",
        "constrain_actions",
        "enforce_dependencies",
        "review_morning_final",
        "compact_final_context",
    ):
        assert trace[key] == prior[key], key
    assert (prior["max_steps"], trace["max_steps"]) == (8, 9)
    assert (prior["repair_budget"], trace["repair_budget"]) == (0, 1)
    for old, new in zip(prior["steps"], trace["steps"][:8], strict=True):
        assert old["worker_request"] == new["worker_request"]
        assert old["model_response"]["text"] == new["model_response"]["text"]
        assert old.get("tool_calls") == new.get("tool_calls")
    rejected = trace["steps"][7]
    assert rejected["response_review"] == prior["response_review"]
    assert rejected["actions"][0]["final"] == prior["final"]
    correction_messages = trace["steps"][8]["worker_request"]["messages"]
    assert rejected["correction_feedback"] in correction_messages
    assert {
        "role": "assistant",
        "content": rejected["model_response"]["text"],
    } in correction_messages
    for step in trace["steps"][:7]:
        assert step["tool_calls"][0]["result_message"] in correction_messages
    expected = deepcopy(prior["final"])
    expected["platforms"][0]["evidence_ids"].remove("msg_issue_blank")
    assert trace["final"] == expected
    assert trace["status"] == "structured_fields_match"
    assert trace["response_review"]["issues"] == []
    assert trace["response_review"]["explanation_word_count"] == 52
    assert trace["response_review"]["checked_summary"] is not None
    assert hashlib.sha256(
        (DIRECTORY / "qwen4-morning-correction.json").read_bytes()
    ).hexdigest() == ("30e84bfb72ba5b9918a74c64137403c421149889119179da82cb284e07347e50")


@pytest.mark.parametrize(
    "name", ["qwen4-morning-correction", "qwen4-morning-explanation-checklist"]
)
def test_morning_correction_preserves_requests_feedback_and_scoped_tool_results(name):
    trace = json.loads((DIRECTORY / f"{name}.json").read_text(encoding="utf-8"))
    messages = deepcopy(trace["initial_messages"])
    policy_indexes = []
    policy = MorningReviewPolicy()
    engine = Copilot()
    feedback_count = 0
    for step in trace["steps"]:
        assert step["policy_before"] == policy.snapshot()
        policy_indexes.append(len(messages))
        messages.append(step["policy_message"])
        expected_messages = messages
        if not policy.pending:
            if trace.get("explanation_checklist"):
                guidance = {"role": "system", "content": MORNING_EXPLANATION_GUIDANCE}
                assert step["explanation_guidance_message"] == guidance
                messages.append(guidance)
            contract = {"role": "system", "content": MORNING_FINAL_GUIDANCE}
            assert step["final_contract_message"] == contract
            messages.append(contract)
            expected_messages, audit = compact_final_messages(messages, policy_indexes)
            assert step["context_reduction"] == audit
        request = step["worker_request"]
        assert request["messages"] == expected_messages
        payload = (json.dumps(request, ensure_ascii=False) + "\n").encode("utf-8")
        assert hashlib.sha256(payload).hexdigest() == step["request_sha256"]
        proposal = json.loads(step["model_response"]["text"])
        Draft202012Validator(request["json_schema"]).validate(proposal)
        assert step["actions"] == [proposal]
        policy.validate_batch([proposal])
        messages.append({"role": "assistant", "content": step["model_response"]["text"]})
        for call in step.get("tool_calls", []):
            assert call["tool_error"] is False
            action = call["action"]
            assert call["tool_result"] == getattr(engine, action["tool"])(**action["arguments"])
            policy.observe(action, call["tool_result"])
            assert call["policy_after"] == policy.snapshot()
            messages.append(call["result_message"])
        if "final" in proposal:
            review = review_morning_final(proposal["final"], trace)
            assert review == step["response_review"]
            assert review["free_text_verification"] == "not_performed"
        if "correction_feedback" in step:
            feedback_count += 1
            assert step["repair_number"] == feedback_count
            feedback = step["correction_feedback"]
            assert feedback["role"] == "user"
            assert (
                json.dumps(step["response_review"]["issues"], ensure_ascii=False)
                in feedback["content"]
            )
            messages.append(feedback)
    assert feedback_count == trace["repair_budget"] == 1
    assert trace["max_steps"] == 9
    assert trace["coverage"]["observed"] == trace["coverage"]["required"] == 7
    assert trace["dependency_policy"] == policy.snapshot()
    assert trace["final"] == trace["steps"][-1]["actions"][0]["final"]
    assert trace["response_review"] == trace["steps"][-1]["response_review"]


def test_explanation_checklist_changes_only_the_first_final_request_input():
    prior = json.loads((DIRECTORY / "qwen4-morning-correction.json").read_text(encoding="utf-8"))
    trace = json.loads(
        (DIRECTORY / "qwen4-morning-explanation-checklist.json").read_text(encoding="utf-8")
    )
    for key in (
        "runtime",
        "task",
        "task_id",
        "model_id",
        "revision",
        "initial_messages",
        "protocol_version",
        "response_timeout_seconds",
        "constrain_actions",
        "enforce_dependencies",
        "review_morning_final",
        "compact_final_context",
        "max_steps",
        "repair_budget",
    ):
        assert trace[key] == prior[key], key
    assert trace["explanation_checklist"] is True
    for old, new in zip(prior["steps"][:7], trace["steps"][:7], strict=True):
        assert old["worker_request"] == new["worker_request"]
        assert old["model_response"]["text"] == new["model_response"]["text"]
        assert old.get("tool_calls") == new.get("tool_calls")
        assert new.get("explanation_guidance_message") is None
    first_final = trace["steps"][7]
    request = deepcopy(first_final["worker_request"])
    assert request["messages"].pop(-2) == {
        "role": "system",
        "content": MORNING_EXPLANATION_GUIDANCE,
    }
    assert request == prior["steps"][7]["worker_request"]
    assert first_final["context_reduction"]["original_message_count"] == 26
    assert first_final["context_reduction"]["retained_message_count"] == 19
    assert first_final["response_review"]["status"] == "rejected"
    assert first_final["response_review"]["explanation_word_count"] == 48
    assert [item["field"] for item in first_final["response_review"]["issues"]] == [
        "lantern_android.evidence_ids"
    ]
    expected = deepcopy(first_final["actions"][0]["final"])
    expected["platforms"][0]["evidence_ids"].remove("msg_issue_blank")
    assert trace["final"] == expected
    assert trace["status"] == "structured_fields_match"
    assert trace["response_review"]["explanation_word_count"] == 48
    assert trace["response_review"]["issues"] == []
    correction = trace["steps"][8]
    assert correction["context_reduction"]["original_message_count"] == 31
    assert correction["context_reduction"]["retained_message_count"] == 23
    assert (
        correction["worker_request"]["messages"].count(
            {"role": "system", "content": MORNING_EXPLANATION_GUIDANCE}
        )
        == 2
    )
    assert (
        hashlib.sha256(
            (DIRECTORY / "qwen4-morning-explanation-checklist.json").read_bytes()
        ).hexdigest()
        == "50cb3f76fef95d6122140b263fb7f7e38ccd7bf76a8720645b5e393820399737"
    )
