"""Exercise the real stdio MCP transport. This is a scripted client, not an LLM agent."""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run(server_command: Path | None = None):
    params = StdioServerParameters(
        command=str(server_command) if server_command else sys.executable,
        args=[] if server_command else ["-m", "csm_copilot.server"],
    )
    calls = [
        ("list_accounts", {}),
        ("get_account_context", {"account_id": "acc_014"}),
        ("check_readiness", {"integration_id": "lantern_android"}),
        (
            "triage_issue",
            {"issue_text": "The offerwall is blank.", "integration_id": "lantern_android"},
        ),
        ("draft_ticket", {"issue_id": "issue_blank"}),
        ("draft_followup", {"integration_id": "lantern_android", "lang": "en"}),
        ("validate_draft", {"text": "We guarantee approval tomorrow."}),
        ("draft_followup", {"integration_id": "lantern_ios", "lang": "en"}),
        ("draft_followup", {"integration_id": "pine_ios", "lang": "zh"}),
        ("friction_digest", {}),
    ]
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            tools = await session.list_tools()
            assert {name for name, _ in calls} == {t.name for t in tools.tools}
            prompts = await session.list_prompts()
            assert "morning_review" in {p.name for p in prompts.prompts}
            prompt = await session.get_prompt("morning_review")
            assert prompt.messages
            feedback_prompt = await session.get_prompt("product_feedback_review")
            assert feedback_prompt.messages
            results = []
            for name, args in calls:
                result = await session.call_tool(name, args)
                assert not result.isError, (name, result)
                payload = result.structuredContent
                assert payload is not None
                results.append({"tool": name, "arguments": args, "result": payload})
            assert results[0]["result"]["accounts"][0]["account_id"] == "acc_014"
            assert results[2]["result"]["decision"] == "blocked"
            assert results[4]["result"]["sent"] is False
            assert results[5]["result"]["contact_history_changed"] is False
            assert "approval_promise" in results[6]["result"]["flags"]
            assert results[5]["result"]["intent"] == "evidence_request"
            assert results[7]["result"]["intent"] == "launch_plan_review"
            assert results[8]["result"]["intent"] == "post_launch_checkin"
            assert "上线时间" not in results[8]["result"]["body"]
            assert results[9]["result"]["cohort_account_count"] == 4
            assert len(results[9]["result"]["themes"]) == 4
            invalid = await session.call_tool("check_readiness", {"integration_id": "missing"})
            assert invalid.isError
            identifier = await session.call_tool("triage_issue", {"issue_text": "issue_callback"})
            assert identifier.isError
            return {
                "transport": "stdio",
                "model_inference": False,
                "server": init.serverInfo.model_dump(),
                "tool_count": len(tools.tools),
                "invalid_id_returns_error": True,
                "identifier_input_returns_error": True,
                "calls": results,
            }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--server-command", type=Path, help="Optional installed console entry point"
    )
    args = parser.parse_args()
    result = asyncio.run(run(args.server_command))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(
        f"PASS: {result['tool_count']} tools, prompt retrieval, invalid-ID error over real stdio MCP."
    )
