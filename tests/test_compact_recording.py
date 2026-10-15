"""Inspect the actual reduced-context recording without running a model."""

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from csm_copilot.morning_review import review_morning_final

DIRECTORY = Path(__file__).resolve().parents[1] / "evidence/model-runs"


def test_recorded_reduction_preserves_tool_work_and_reconstructs_prior_final_history():
    before = json.loads((DIRECTORY / "qwen4-morning-field-review.json").read_text(encoding="utf-8"))
    after = json.loads(
        (DIRECTORY / "qwen4-morning-compact-context.json").read_text(encoding="utf-8")
    )
    for key in (
        "runtime",
        "initial_messages",
        "prompt_sha256",
        "task",
        "task_id",
        "model_id",
        "revision",
        "max_steps",
        "repair_budget",
        "response_timeout_seconds",
        "protocol_version",
        "enforce_dependencies",
        "constrain_actions",
        "review_morning_final",
        "dependency_policy",
    ):
        assert before[key] == after[key], key
    assert after["compact_final_context"] is True
    assert len(after["steps"]) == 8
    assert after["coverage"]["observed"] == after["coverage"]["required"] == 7
    for old, new in zip(before["steps"][:7], after["steps"][:7], strict=True):
        for key in (
            "worker_request",
            "actions",
            "tool_calls",
            "generation_schema",
            "policy_before",
        ):
            assert old[key] == new[key]
        assert "context_reduction" not in new
        assert old["model_response"]["text"] == new["model_response"]["text"]

    old, new = before["steps"][-1], after["steps"][-1]
    audit = new["context_reduction"]
    assert audit["method"] == "superseded_policy_messages_v1"
    assert audit["original_message_count"] == 25 and audit["retained_message_count"] == 18
    omitted_positions = [2, 5, 8, 11, 14, 17, 20]
    assert [item["original_index"] for item in audit["omitted_messages"]] == omitted_positions
    retained = new["worker_request"]["messages"]
    assert audit["retained_message_indexes"] == [i for i in range(25) if i not in omitted_positions]
    restored = [None] * 25
    for index, message in zip(audit["retained_message_indexes"], retained, strict=True):
        restored[index] = message
    for omitted in audit["omitted_messages"]:
        restored[omitted["original_index"]] = omitted["message"]
    assert restored == old["worker_request"]["messages"]
    assert retained[-2:] == restored[-2:]
    assert new["final_contract_message"] == old["final_contract_message"]
    assert new["generation_schema"] == old["generation_schema"]
    assert new["worker_request"]["json_schema"] == old["worker_request"]["json_schema"]
    for step in after["steps"]:
        payload = (json.dumps(step["worker_request"], ensure_ascii=False) + "\n").encode("utf-8")
        assert hashlib.sha256(payload).hexdigest() == step["request_sha256"]
        assert "correction_feedback" not in step


def test_reduced_context_recording_retains_the_same_field_failure():
    before = json.loads((DIRECTORY / "qwen4-morning-field-review.json").read_text(encoding="utf-8"))
    raw = (DIRECTORY / "qwen4-morning-compact-context.json").read_bytes()
    assert (
        hashlib.sha256(raw).hexdigest()
        == "d22d9e66343c50b265720a358a1ae2ab62b26bbe154899d90c8b26ffecd967d6"
    )
    after = json.loads(raw)
    old, new = before["steps"][-1]["model_response"], after["steps"][-1]["model_response"]
    assert (old["input_tokens"], new["input_tokens"]) == (9386, 7728)
    assert (old["output_tokens"], new["output_tokens"]) == (314, 322)
    assert (old["seconds"], new["seconds"]) == (405.461, 94.323)
    assert new["schema_constrained"] is True and new["token_limit_reached"] is False
    proposal = json.loads(new["text"])
    Draft202012Validator(after["steps"][-1]["generation_schema"]).validate(proposal)
    assert proposal["final"] == after["final"]
    assert after["steps"][-1]["actions"] == [proposal]
    for key in before["final"]:
        if key != "explanation":
            assert before["final"][key] == after["final"][key], key
    assert before["final"]["explanation"] != after["final"]["explanation"]
    review = review_morning_final(after["final"], after)
    assert review == after["response_review"] == after["steps"][-1]["response_review"]
    assert review["status"] == after["status"] == "rejected"
    assert review["issues"] == before["response_review"]["issues"]
    assert len(review["issues"]) == 1
    assert review["issues"][0]["field"] == "lantern_android.evidence_ids"
    assert review["checked_summary"] is None
    assert review["free_text_verification"] == "not_performed"
    assert review["explanation_word_count"] == 52
