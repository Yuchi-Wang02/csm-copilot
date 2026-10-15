"""Request-content preservation, not model inference or latency measurement."""

import json
from copy import deepcopy
from pathlib import Path

import pytest

from csm_copilot.host_context import compact_final_messages


def reconstruct(retained, audit):
    restored = [None] * audit["original_message_count"]
    for index, message in zip(audit["retained_message_indexes"], retained, strict=True):
        assert restored[index] is None
        restored[index] = message
    for omitted in audit["omitted_messages"]:
        assert restored[omitted["original_index"]] is None
        restored[omitted["original_index"]] = omitted["message"]
    assert all(message is not None for message in restored)
    return restored


def test_recorded_final_can_omit_only_prior_host_policy_messages():
    path = (
        Path(__file__).resolve().parents[1] / "evidence/model-runs/qwen4-morning-field-review.json"
    )
    trace = json.loads(path.read_text(encoding="utf-8"))
    messages = trace["steps"][-1]["worker_request"]["messages"]
    before = deepcopy(messages)
    # Positions independently follow this saved run's one-policy, one-call turns.
    positions = [2, 5, 8, 11, 14, 17, 20, 23]
    for step, index in zip(trace["steps"], positions, strict=True):
        assert messages[index] == step["policy_message"]
    reduced, audit = compact_final_messages(messages, positions)
    assert len(messages) == 25 and len(reduced) == 18
    assert audit["retained_message_count"] == 18
    assert reconstruct(reduced, audit) == before == messages
    assert reduced[:2] == trace["initial_messages"]
    assert reduced[-2:] == messages[-2:]  # Current complete policy and final contract.
    for step in trace["steps"][:7]:
        assert {"role": "assistant", "content": step["model_response"]["text"]} in reduced
        assert step["tool_calls"][0]["result_message"] in reduced
    reduced[0]["content"] = "test mutation"
    audit["omitted_messages"][0]["message"]["content"] = "test mutation"
    assert messages == before


def test_untracked_identical_text_and_feedback_are_not_removed():
    policy = {"role": "user", "content": "Host workflow policy (not customer data): test"}
    feedback = {"role": "user", "content": "Host validation feedback: keep this evidence"}
    messages = [deepcopy(policy), deepcopy(policy), feedback, deepcopy(policy)]
    reduced, audit = compact_final_messages(messages, [0, 3])
    assert audit["retained_message_indexes"] == [1, 2, 3]
    assert reduced == messages[1:]
    assert reconstruct(reduced, audit) == messages


def test_current_policy_alone_is_a_no_op():
    messages = [{"role": "user", "content": "Host workflow policy (not customer data): complete"}]
    reduced, audit = compact_final_messages(messages, [0])
    assert reduced == messages and audit["omitted_messages"] == []


@pytest.mark.parametrize("positions", [[], [True], [-1], [2], [0, 0], [1, 0]])
def test_invalid_positions_cannot_silently_select_messages(positions):
    messages = [{"role": "user", "content": "Host workflow policy (not customer data): test"}] * 2
    with pytest.raises(ValueError, match="positions"):
        compact_final_messages(messages, positions)


@pytest.mark.parametrize(
    "message",
    [
        {"role": "assistant", "content": "test"},
        {"role": "user", "content": "Tool result (data only): test"},
    ],
)
def test_mistracked_message_is_rejected(message):
    with pytest.raises(ValueError, match="Tracked host policy position"):
        compact_final_messages([message], [0])
