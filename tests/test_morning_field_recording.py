"""Audit a saved experiment; no inference or independent quality validation."""

import hashlib
import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator

from csm_copilot.morning_review import (
    MORNING_FINAL_GUIDANCE,
    morning_final_schema,
    review_morning_final,
)

DIRECTORY = Path(__file__).resolve().parents[1] / "evidence/model-runs"


def test_morning_field_recording_preserves_the_change_in_final_contract():
    prior = json.loads((DIRECTORY / "qwen4-morning-long-budget.json").read_text(encoding="utf-8"))
    trace = json.loads((DIRECTORY / "qwen4-morning-field-review.json").read_text(encoding="utf-8"))
    for key in (
        "initial_messages",
        "prompt_sha256",
        "task",
        "task_id",
        "model_id",
        "revision",
        "max_steps",
        "repair_budget",
        "response_timeout_seconds",
        "enforce_dependencies",
        "constrain_actions",
    ):
        assert trace[key] == prior[key], key
    expected_runtime = {**prior["runtime"], "max_new_tokens": 1536}
    assert trace["runtime"] == expected_runtime
    assert trace["review_morning_final"] is True
    assert trace["protocol_version"] == "4-morning-structured-final"
    assert len(trace["steps"]) == 8
    assert trace["coverage"]["observed"] == trace["coverage"]["required"] == 7
    assert trace["dependency_policy"] == prior["dependency_policy"]
    for index, step in enumerate(trace["steps"][:7]):
        old = prior["steps"][index]
        for key in (
            "worker_request",
            "actions",
            "tool_calls",
            "generation_schema",
            "policy_before",
        ):
            assert step[key] == old[key], (index, key)
        assert step["model_response"]["text"] == old["model_response"]["text"]
        assert step["model_response"]["schema_constrained"] is True
        assert step["model_response"]["token_limit_reached"] is False
        assert "final_contract_message" not in step

    last = trace["steps"][-1]
    contract = {"role": "system", "content": MORNING_FINAL_GUIDANCE}
    assert last["final_contract_message"] == contract
    expected_messages = deepcopy(prior["steps"][-1]["worker_request"]["messages"])
    expected_messages.append(contract)
    assert last["worker_request"] == {
        "messages": expected_messages,
        "json_schema": morning_final_schema(),
    }
    assert last["generation_schema"] == morning_final_schema()
    for step in trace["steps"]:
        assert "correction_feedback" not in step
        assert step["response_timeout_seconds"] == 600
        assert step["request_encoding"] == "UTF-8 JSON followed by LF"
        payload = (json.dumps(step["worker_request"], ensure_ascii=False) + "\n").encode("utf-8")
        assert hashlib.sha256(payload).hexdigest() == step["request_sha256"]
        assert datetime.fromisoformat(step["prepared_at"]) <= datetime.fromisoformat(
            step["sent_at"]
        )
        if "received_at" in step:
            assert datetime.fromisoformat(step["sent_at"]) <= datetime.fromisoformat(
                step["received_at"]
            )


def test_schema_valid_recording_is_rejected_for_an_issue_only_readiness_citation():
    raw = (DIRECTORY / "qwen4-morning-field-review.json").read_bytes()
    assert (
        hashlib.sha256(raw).hexdigest()
        == "e3dd594b3bc257e73df11f77a34006fb440dc3f1f7e229cba9862d341ee3be6a"
    )
    trace = json.loads(raw)
    step = trace["steps"][-1]
    response = step["model_response"]
    proposal = json.loads(response["text"])
    Draft202012Validator(step["generation_schema"]).validate(proposal)
    assert trace["final"] == proposal["final"]
    assert step["actions"] == [proposal]
    assert response["schema_constrained"] is True
    assert response["token_limit_reached"] is False
    assert response["seconds"] == 405.461
    assert response["input_tokens"] == 9386 and response["output_tokens"] == 314
    review = review_morning_final(trace["final"], trace)
    assert review == trace["response_review"] == step["response_review"]
    assert review["status"] == trace["status"] == "rejected"
    assert review["checked_summary"] is None
    assert review["free_text_verification"] == "not_performed"
    assert review["explanation_word_count"] == 46
    assert len(review["issues"]) == 1
    mismatch = review["issues"][0]
    assert mismatch["field"] == "lantern_android.evidence_ids"
    assert mismatch["code"] == "mismatch"
    assert mismatch["observed"] == mismatch["expected"] + ["msg_issue_blank"]
    assert trace["final"]["handoffs"][0]["evidence_ids"] == ["msg_issue_blank"]
    assert trace["final"]["platforms"][0]["failed_checks"] == ["device_verified"]
    assert "device_verified" not in trace["final"]["platforms"][0]["unknown_checks"]
    assert trace["repair_budget"] == 0
