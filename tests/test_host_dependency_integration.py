"""Scripted worker responses through the actual host and real MCP stdio server.

These are software integration tests, not model inference or model recordings.
"""

import asyncio
import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest
from jsonschema import Draft202012Validator

from scripts import run_local_host


@pytest.mark.parametrize(
    "mode,expected_status",
    [
        ("match", "structured_fields_match"),
        ("conflation", "rejected"),
        ("wrong_action", "rejected"),
        ("missing_field", "rejected"),
        ("corrected", "structured_fields_match"),
        ("unsupported_prose", "structured_fields_match"),
        ("unconstrained", "structured_fields_match"),
    ],
)
def test_morning_final_contract_through_real_mcp(tmp_path, monkeypatch, mode, expected_status):
    from test_morning_final import morning_example

    from csm_copilot.morning_review import MORNING_FINAL_GUIDANCE, morning_final_schema

    correct, _ = morning_example()

    class ReviewedWorker(ScriptedWorker):
        final_count = 0

        def write(self, data):
            request = json.loads(data)
            if request["messages"][-1]["content"] != MORNING_FINAL_GUIDANCE:
                super().write(data)
                return
            self.requests.append(request)
            self.final_count += 1
            if mode == "unconstrained":
                assert "json_schema" not in request
            else:
                assert request["json_schema"] == morning_final_schema()
            answer = deepcopy(correct)
            if mode == "conflation" or (mode == "corrected" and self.final_count == 1):
                answer["platforms"][0]["failed_checks"] = []
                answer["platforms"][0]["unknown_checks"].append("device_verified")
            elif mode == "wrong_action":
                answer["platforms"][0]["followup_intent"] = "launch_plan_review"
            elif mode == "missing_field":
                answer["handoffs"][0]["missing_fields"].remove("redacted_logs")
            elif mode == "unsupported_prose":
                answer["explanation"] = "Both launches are approved and revenue is guaranteed."
            self.responses.append({"text": json.dumps({"final": answer})})

    worker = ReviewedWorker("happy_path" if mode == "unconstrained" else "constrained_happy")

    async def scripted_start(_args, _env):
        return worker

    monkeypatch.setattr(run_local_host, "start_worker", scripted_start)
    args = SimpleNamespace(
        model_python=sys.executable,
        model_path=tmp_path,
        model_id="SCRIPTED-NO-MODEL",
        revision="test",
        protocol="batch",
        task="morning_review",
        max_steps=9,
        response_timeout_seconds=180,
        repair_attempts=1 if mode == "corrected" else 0,
        sequence_dependencies=False,
        enforce_dependencies=True,
        constrain_actions=mode != "unconstrained",
        constrain_final=False,
        review_morning_final=True,
        max_new_tokens=768,
        output=tmp_path / "review.json",
    )
    asyncio.run(asyncio.wait_for(run_local_host.run(args), timeout=45))
    trace = json.loads(args.output.read_text(encoding="utf-8"))
    assert trace["status"] == expected_status
    assert trace["protocol_version"] == "4-morning-structured-final"
    assert trace["coverage"]["observed"] == 7 and trace["review_morning_final"] is True
    assert worker.returncode == 0
    tool_turns = 4 if mode == "unconstrained" else 7
    assert all("final_contract_message" not in step for step in trace["steps"][:tool_turns])
    for step in trace["steps"][tool_turns:]:
        assert step["final_contract_message"] == step["worker_request"]["messages"][-1]
        assert step["final_contract_message"]["content"] == MORNING_FINAL_GUIDANCE
        assert step["final_contract_message"]["role"] == "system"
        if mode == "unconstrained":
            assert "generation_schema" not in step
        else:
            assert step["generation_schema"] == morning_final_schema()
        assert step["response_review"]["free_text_verification"] == "not_performed"
    if mode == "corrected":
        assert len(trace["steps"]) == 9
        rejected = trace["steps"][7]
        assert rejected["response_review"]["status"] == "rejected"
        assert "device_verified" in rejected["correction_feedback"]["content"]
        assert trace["steps"][-1]["actions"][0]["final"] == correct
    else:
        assert len(trace["steps"]) == tool_turns + 1
        assert not any("correction_feedback" in step for step in trace["steps"])
    if mode == "unsupported_prose":
        assert "guaranteed" in trace["final"]["explanation"]
        assert "guaranteed" not in trace["response_review"]["checked_summary"]
    if mode == "match":
        baseline = ScriptedWorker("constrained_happy")

        async def baseline_start(_args, _env):
            return baseline

        monkeypatch.setattr(run_local_host, "start_worker", baseline_start)
        args.review_morning_final = False
        args.output = tmp_path / "baseline.json"
        asyncio.run(asyncio.wait_for(run_local_host.run(args), timeout=45))
        assert worker.requests[:7] == baseline.requests[:7], "No new instructions before final work"
        assert worker.requests[7] != baseline.requests[7]


@pytest.mark.parametrize(
    "extra,exit_code",
    [
        ([], 2),
        (["--enforce-dependencies"], 2),
        (["--enforce-dependencies", "--task", "morning_review"], 1),
    ],
)
def test_morning_final_cli_requires_policy_and_fails_on_rejected_fields(
    tmp_path, monkeypatch, extra, exit_code
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "host",
            "--model-path",
            str(tmp_path),
            "--model-id",
            "test",
            "--revision",
            "test",
            "--output",
            str(tmp_path / "new.json"),
            "--review-morning-final",
            *extra,
        ],
    )
    calls = []

    async def fake_run(args):
        calls.append(args.review_morning_final)
        return "rejected"

    monkeypatch.setattr(run_local_host, "run", fake_run)
    with pytest.raises(SystemExit) as exc:
        run_local_host.main()
    assert exc.value.code == exit_code
    assert calls == ([True] if exit_code == 1 else [])


class ScriptedWorker:
    def __init__(self, mode):
        self.mode = mode
        self.stdin = self.stdout = self
        self.returncode = None
        self.responses = [{"runtime": "scripted test worker; no model inference"}]
        self.requests = []

    def write(self, data):
        request = json.loads(data)
        self.requests.append(request)
        content = request["messages"][-1]["content"]
        policy = json.loads(content[content.index("{") :])
        if self.mode == "premature_final":
            actions = {"final": "Done without checking"}
        elif self.mode == "dependent_batch":
            actions = [
                {"tool": "list_accounts", "arguments": {}},
                {"tool": "get_account_context", "arguments": {"account_id": "acc_014"}},
            ]
        elif (
            self.mode in ("unknown_account", "constrained_unknown_account")
            and policy["stage"] == "awaiting_context"
        ):
            actions = {"tool": "get_account_context", "arguments": {"account_id": "12345"}}
        elif self.mode == "mixed_scope" and policy["stage"] == "reviewing":
            actions = [
                policy["pending_actions"][0],
                {"tool": "draft_ticket", "arguments": {"issue_id": "foreign-issue"}},
            ]
        elif policy["pending_actions"]:
            if self.mode.startswith("constrained_"):
                actions = policy["pending_actions"][0]
                if actions["tool"] == "list_accounts":
                    actions["arguments"] = {}
            else:
                actions = policy["pending_actions"][:4]
        else:
            actions = {"final": "Scripted test completion; nothing was sent or submitted."}
        if self.mode == "constrained_happy":
            Draft202012Validator(request["json_schema"]).validate(actions)
        self.responses.append({"text": json.dumps(actions)})

    async def drain(self):
        pass

    async def readline(self):
        return (json.dumps(self.responses.pop(0)) + "\n").encode()

    def terminate(self):
        self.returncode = 0

    async def wait(self):
        return self.returncode


class LifecycleWorker(ScriptedWorker):
    """Observe persisted files at the dispatch/wait boundaries, then inject a fault."""

    def __init__(self, output, fault, fail_turn):
        super().__init__("constrained_happy")
        self.output, self.fault, self.fail_turn = output, fault, fail_turn
        self.payloads = []
        self.waited = False

    def write(self, data):
        snapshot = json.loads(self.output.read_text(encoding="utf-8"))
        step = snapshot["steps"][-1]
        assert snapshot["status"] == "request_prepared"
        assert step["request_state"] == "prepared"
        assert step["worker_request"] == json.loads(data)
        assert step["request_sha256"] == hashlib.sha256(data).hexdigest()
        self.payloads.append(data)
        if self.fault == "dispatch" and len(self.payloads) == self.fail_turn:
            raise BrokenPipeError("scripted dispatch failure")
        super().write(data)

    async def readline(self):
        if self.requests:
            snapshot = json.loads(self.output.read_text(encoding="utf-8"))
            assert snapshot["status"] == "waiting_for_response"
            assert snapshot["steps"][-1]["request_state"] == "sent"
            if len(self.requests) == self.fail_turn:
                if self.fault == "timeout":
                    await asyncio.Event().wait()
                if self.fault == "eof":
                    return b""
                if self.fault == "json":
                    return b"invalid worker envelope\n"
                if self.fault == "unicode":
                    return b"\xff\n"
                if self.fault == "cancel":
                    raise asyncio.CancelledError()
        return await super().readline()

    async def wait(self):
        self.waited = True
        return await super().wait()


@pytest.mark.parametrize(
    "fault,fail_turn,status,completed",
    [
        ("none", 99, "final_response", 7),
        ("timeout", 1, "response_timeout", 0),
        ("timeout", 8, "response_timeout", 7),
        ("eof", 1, "worker_response_error", 0),
        ("json", 1, "worker_response_error", 0),
        ("unicode", 1, "worker_response_error", 0),
        ("dispatch", 1, "host_error", 0),
        ("cancel", 1, "cancelled", 0),
    ],
)
def test_request_lifecycle_survives_worker_failures(
    tmp_path, monkeypatch, fault, fail_turn, status, completed
):
    output = tmp_path / "scripted-lifecycle.json"
    worker = LifecycleWorker(output, fault, fail_turn)

    async def scripted_start(_args, _env):
        return worker

    monkeypatch.setattr(run_local_host, "start_worker", scripted_start)
    args = SimpleNamespace(
        model_python=sys.executable,
        model_path=tmp_path,
        model_id="scripted-test-worker-NOT-A-MODEL",
        revision="test",
        protocol="batch",
        task="morning_review",
        max_steps=8,
        response_timeout_seconds=0.05,
        repair_attempts=2,
        sequence_dependencies=False,
        enforce_dependencies=True,
        constrain_actions=True,
        constrain_final=False,
        max_new_tokens=768,
        output=output,
    )

    async def exercise():
        if fault == "cancel":
            with pytest.raises(asyncio.CancelledError):
                await run_local_host.run(args)
        elif fault == "dispatch":
            with pytest.raises(ExceptionGroup):
                await run_local_host.run(args)
        else:
            assert await run_local_host.run(args) == status

    asyncio.run(asyncio.wait_for(exercise(), timeout=45))
    trace = json.loads(output.read_text(encoding="utf-8"))
    assert trace["trace_schema_version"] == 2
    assert trace["status"] == status
    assert trace["coverage"]["observed"] == completed
    assert worker.returncode == 0 and worker.waited
    assert len(trace["steps"]) == len(worker.payloads) == min(fail_turn, 8)
    assert all("correction_feedback" not in step for step in trace["steps"])
    for step, payload in zip(trace["steps"], worker.payloads, strict=True):
        assert step["worker_request"] == json.loads(payload), "Earlier inputs stay detached"
        assert step["request_sha256"] == hashlib.sha256(payload).hexdigest()
        assert (json.dumps(step["worker_request"], ensure_ascii=False) + "\n").encode() == payload
    last = trace["steps"][-1]
    if fault == "none":
        assert all(step["request_state"] == "response_received" for step in trace["steps"])
        assert trace["final"]
    else:
        assert "model_response" not in last and "actions" not in last
        assert trace["final"] is None
    if fault == "timeout":
        assert trace["error_type"] == "TimeoutError"
        assert last["request_state"] == "response_timeout"
        assert last["response_error"]["partial_output_captured"] is False
        assert last["response_error"]["timeout_seconds"] == 0.05
        if completed == 7:
            assert trace["dependency_policy"]["stage"] == "complete"
            assert "final" in last["worker_request"]["json_schema"]["properties"]
    if fault == "dispatch":
        assert last["failure_phase"] == "dispatch" and "sent_at" not in last
        assert {cause["type"] for cause in trace["error_causes"]} == {"BrokenPipeError"}
    if fault in ("eof", "json", "unicode"):
        expected = {
            "eof": "RuntimeError",
            "json": "JSONDecodeError",
            "unicode": "UnicodeDecodeError",
        }[fault]
        assert last["response_error"]["type"] == expected
        assert last["request_state"] == "response_error"
    if fault == "json":
        assert last["worker_response_text"] == "invalid worker envelope\n"
    if fault == "cancel":
        assert last["request_state"] == "cancelled"


def test_atomic_snapshot_failure_preserves_prior_file_and_unrelated_temp(tmp_path, monkeypatch):
    output = tmp_path / "trace.json"
    unrelated = tmp_path / ".trace.json.someone-else.tmp"
    unrelated.write_text("keep", encoding="utf-8")
    run_local_host.save_trace(output, {"status": "prior"})

    def fail_replace(self, target):
        raise PermissionError("scripted replace failure")

    monkeypatch.setattr(Path, "replace", fail_replace)
    with pytest.raises(PermissionError):
        run_local_host.save_trace(output, {"status": "new"})
    assert json.loads(output.read_text(encoding="utf-8")) == {"status": "prior"}
    assert unrelated.read_text(encoding="utf-8") == "keep"
    assert sorted(path.name for path in tmp_path.iterdir()) == [unrelated.name, output.name]


@pytest.mark.parametrize("budget,exit_code", [(None, 1), ("600", 1), ("0", 2), ("601", 2)])
def test_cli_validates_and_records_timeout_budget(tmp_path, monkeypatch, budget, exit_code):
    argv = [
        "host",
        "--model-path",
        str(tmp_path),
        "--model-id",
        "test",
        "--revision",
        "test",
        "--output",
        str(tmp_path / "new.json"),
    ]
    if budget is not None:
        argv += ["--response-timeout-seconds", budget]
    called = []

    async def fake_run(args):
        called.append(args.response_timeout_seconds)
        return "response_timeout"

    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setattr(run_local_host, "run", fake_run)
    with pytest.raises(SystemExit) as error:
        run_local_host.main()
    assert error.value.code == exit_code
    assert called == ([180 if budget is None else int(budget)] if exit_code == 1 else [])


@pytest.mark.parametrize(
    "mode,status,call_count",
    [
        ("happy_path", "final_response", 7),
        ("dependent_batch", "policy_rejected", 0),
        ("premature_final", "policy_rejected", 0),
        ("unknown_account", "policy_rejected", 1),
        ("mixed_scope", "policy_rejected", 2),
        ("constrained_happy", "final_response", 7),
        ("constrained_unknown_account", "policy_rejected", 1),
    ],
)
def test_host_enforces_dependencies_before_real_mcp_calls(
    tmp_path, monkeypatch, mode, status, call_count
):
    worker = ScriptedWorker(mode)

    async def scripted_start(_args, _env):
        return worker

    monkeypatch.setattr(run_local_host, "start_worker", scripted_start)
    args = SimpleNamespace(
        model_python=sys.executable,
        model_path=tmp_path,
        model_id="scripted-test-worker-NOT-A-MODEL",
        revision="test",
        protocol="batch",
        task="morning_review",
        max_steps=8,
        response_timeout_seconds=180,
        repair_attempts=0,
        sequence_dependencies=False,
        enforce_dependencies=True,
        constrain_actions=mode.startswith("constrained_"),
        constrain_final=False,
        max_new_tokens=768,
        output=tmp_path / "temporary-test-trace.json",
    )
    asyncio.run(asyncio.wait_for(run_local_host.run(args), timeout=45))
    trace = json.loads(args.output.read_text(encoding="utf-8"))
    calls = [call for step in trace["steps"] for call in step.get("tool_calls", [])]
    assert trace["status"] == status
    assert len(calls) == call_count
    assert trace["coverage"]["observed"] == call_count
    assert all(call["tool_error"] is False for call in calls)
    assert all("policy_message" in step for step in trace["steps"])
    assert worker.returncode == 0
    if mode in ("happy_path", "constrained_happy"):
        assert trace["dependency_policy"]["stage"] == "complete"
        assert len(trace["dependency_policy"]["completed_actions"]) == 7
        assert calls[0]["tool_result"]["accounts"][0]["account_id"] == "acc_014"
        assert calls[1]["action"]["arguments"]["account_id"] == "acc_014"
        assert [len(step.get("tool_calls", [])) for step in trace["steps"]] == (
            [1] * 7 + [0] if mode == "constrained_happy" else [1, 1, 4, 1, 0]
        )
    else:
        assert trace["final"] is None
        assert "policy_error" in trace["steps"][-1]
        assert trace["dependency_policy"]["final_allowed"] is False
    if mode.startswith("constrained_"):
        assert all("generation_schema" in step for step in trace["steps"])
        assert all(
            "choose exactly one pending action" in step["policy_message"]["content"]
            for step in trace["steps"]
        )
        assert trace["steps"][0]["generation_schema"] == worker.requests[0]["json_schema"]
    else:
        assert all("generation_schema" not in step for step in trace["steps"])
        assert "choose up to four pending actions" in trace["steps"][0]["policy_message"]["content"]


@pytest.mark.parametrize("fault", ["tool_error", "wrong_result_scope"])
def test_real_host_preserves_pending_work_after_injected_result_fault(tmp_path, monkeypatch, fault):
    worker = ScriptedWorker("happy_path")

    async def scripted_start(_args, _env):
        return worker

    original_session = run_local_host.ClientSession

    class FaultSession(original_session):
        injected = False

        async def call_tool(self, name, arguments=None, **kwargs):
            result = await super().call_tool(name, arguments, **kwargs)
            if name == "check_readiness" and not self.injected:
                self.injected = True
                result = result.model_copy(deep=True)
                if fault == "tool_error":
                    result.isError = True
                else:
                    result.structuredContent["integration_id"] = "different-integration"
            return result

    monkeypatch.setattr(run_local_host, "start_worker", scripted_start)
    monkeypatch.setattr(run_local_host, "ClientSession", FaultSession)
    args = SimpleNamespace(
        model_python=sys.executable,
        model_path=tmp_path,
        model_id="scripted-test-worker-NOT-A-MODEL",
        revision="test",
        protocol="batch",
        task="morning_review",
        max_steps=8,
        response_timeout_seconds=180,
        repair_attempts=0,
        sequence_dependencies=False,
        enforce_dependencies=True,
        constrain_actions=False,
        constrain_final=False,
        max_new_tokens=768,
        output=tmp_path / "temporary-fault-test-trace.json",
    )
    asyncio.run(asyncio.wait_for(run_local_host.run(args), timeout=45))
    trace = json.loads(args.output.read_text(encoding="utf-8"))
    calls = [call for step in trace["steps"] for call in step.get("tool_calls", [])]
    if fault == "tool_error":
        assert trace["status"] == "final_response"
        assert len(calls) == 8
        assert calls[2]["tool_error"] is True
        assert len(calls[2]["policy_after"]["completed_actions"]) == 2
        assert calls[6]["action"] == calls[2]["action"]
        assert len(trace["dependency_policy"]["completed_actions"]) == 7
        assert trace["coverage"]["observed"] == 7
    else:
        assert trace["status"] == "policy_result_rejected"
        assert len(calls) == 3, "Stop before later actions in the accepted batch"
        assert "policy_result_error" in calls[-1]
        assert len(trace["dependency_policy"]["completed_actions"]) == 2
        assert len(trace["dependency_policy"]["pending_actions"]) == 5
        assert trace["final"] is None
