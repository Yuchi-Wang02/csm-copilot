"""A scripted MCP check must fail when its peer accepts requests but never replies."""

import asyncio
from contextlib import asynccontextmanager

import anyio
from mcp.shared.exceptions import McpError

from scripts import mcp_smoke


def test_unresponsive_peer_reports_a_response_timeout_and_closes_streams(monkeypatch):
    observed = []
    closed = []

    @asynccontextmanager
    async def silent_peer(_params):
        incoming_send, incoming_receive = anyio.create_memory_object_stream(1)
        outgoing_send, outgoing_receive = anyio.create_memory_object_stream(1)

        async def consume_without_reply():
            async for message in outgoing_receive:
                observed.append(message)

        try:
            async with incoming_send, incoming_receive, outgoing_send, outgoing_receive:
                async with anyio.create_task_group() as group:
                    group.start_soon(consume_without_reply)
                    try:
                        yield incoming_receive, outgoing_send
                    finally:
                        group.cancel_scope.cancel()
        finally:
            closed.append(True)

    monkeypatch.setattr(mcp_smoke, "stdio_client", silent_peer)
    monkeypatch.setattr(mcp_smoke, "REQUEST_TIMEOUT_SECONDS", 0.05, raising=False)

    def leaves(error):
        if isinstance(error, BaseExceptionGroup):
            return [leaf for child in error.exceptions for leaf in leaves(child)]
        return [error]

    async def exercise():
        try:
            await asyncio.wait_for(mcp_smoke.run(), timeout=2)
        except Exception as error:
            failures = leaves(error)
            assert any(
                isinstance(failure, McpError)
                and "Timed out while waiting for response" in str(failure)
                for failure in failures
            ), repr(failures)
        else:
            raise AssertionError("An unresponsive peer must not produce a successful transcript")

    asyncio.run(exercise())
    assert observed, "The initialization request must reach the peer"
    assert closed == [True]
