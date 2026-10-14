"""Scripted worker responses through the actual host and real MCP stdio server.

These are software integration tests, not model inference or model recordings.
"""

import asyncio
import json
import sys
from types import SimpleNamespace

import pytest

from scripts import run_local_host


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
        elif self.mode == "unknown_account" and policy["stage"] == "awaiting_context":
            actions = {"tool": "get_account_context", "arguments": {"account_id": "12345"}}
        elif self.mode == "mixed_scope" and policy["stage"] == "reviewing":
            actions = [
                policy["pending_actions"][0],
                {"tool": "draft_ticket", "arguments": {"issue_id": "foreign-issue"}},
            ]
        elif policy["pending_actions"]:
            actions = policy["pending_actions"][:4]
        else:
            actions = {"final": "Scripted test completion; nothing was sent or submitted."}
        self.responses.append({"text": json.dumps(actions)})

    async def drain(self):
        pass

    async def readline(self):
        return (json.dumps(self.responses.pop(0)) + "\n").encode()

    def terminate(self):
        self.returncode = 0

    async def wait(self):
        return self.returncode


@pytest.mark.parametrize(
    "mode,status,call_count",
    [
        ("happy_path", "final_response", 7),
        ("dependent_batch", "policy_rejected", 0),
        ("premature_final", "policy_rejected", 0),
        ("unknown_account", "policy_rejected", 1),
        ("mixed_scope", "policy_rejected", 2),
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
        repair_attempts=0,
        sequence_dependencies=False,
        enforce_dependencies=True,
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
    if mode == "happy_path":
        assert trace["dependency_policy"]["stage"] == "complete"
        assert len(trace["dependency_policy"]["completed_actions"]) == 7
        assert calls[0]["tool_result"]["accounts"][0]["account_id"] == "acc_014"
        assert calls[1]["action"]["arguments"]["account_id"] == "acc_014"
        assert [len(step.get("tool_calls", [])) for step in trace["steps"]] == [1, 1, 4, 1, 0]
    else:
        assert trace["final"] is None
        assert "policy_error" in trace["steps"][-1]
        assert trace["dependency_policy"]["final_allowed"] is False


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
        repair_attempts=0,
        sequence_dependencies=False,
        enforce_dependencies=True,
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
