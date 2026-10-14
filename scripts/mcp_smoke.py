"""Exercise the real stdio MCP transport. This is a scripted client, not an LLM agent."""

import argparse
import asyncio
import json
import sys
from datetime import timedelta
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

REQUEST_TIMEOUT_SECONDS = 30


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
        ("triage_issue", {"issue_text": "Please send the blanket invoice for our annual plan."}),
        ("triage_issue", {"issue_text": "Android页面blank，请协助排查。"}),
        ("triage_issue", {"issue_text": "No offers is not our problem. Please explain invoicing."}),
        ("triage_issue", {"issue_text": "不是没有广告的问题，奖励回调返回405。"}),
        ("list_accounts", {"as_of": "2026-10-17T09:00:00Z"}),
        (
            "triage_issue",
            {"issue_text": "The reward callback is not our problem. Please explain invoicing."},
        ),
        ("triage_issue", {"issue_text": "不是奖励回调的问题，广告墙空白。"}),
        ("triage_issue", {"issue_text": "Callbacks are not failing. Please explain invoicing."}),
    ]
    async with stdio_client(params) as (read, write):
        async with ClientSession(
            read, write, read_timeout_seconds=timedelta(seconds=REQUEST_TIMEOUT_SECONDS)
        ) as session:
            init = await session.initialize()
            assert init.instructions
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
            assert results[0]["result"]["time_basis"] == "dataset_snapshot"
            assert results[2]["result"]["decision"] == "blocked"
            assert results[4]["result"]["sent"] is False
            assert [r["field"] for r in results[4]["result"]["collection_requests"]] == results[4][
                "result"
            ]["missing_fields"]
            assert "not verified" in results[4]["result"]["collection_boundary"]
            assert results[5]["result"]["contact_history_changed"] is False
            assert "approval_promise" in results[6]["result"]["flags"]
            assert results[5]["result"]["intent"] == "evidence_request"
            assert results[7]["result"]["intent"] == "launch_plan_review"
            assert results[8]["result"]["intent"] == "post_launch_checkin"
            assert "上线时间" not in results[8]["result"]["body"]
            assert results[9]["result"]["cohort_account_count"] == 4
            assert len(results[9]["result"]["themes"]) == 4
            assert results[10]["result"]["route"] == "clarify_scope"
            assert results[10]["result"]["candidates"][0]["category"] == "unknown"
            assert results[11]["result"]["candidates"][0]["category"] == "no_offers"
            assert results[12]["result"]["route"] == "clarify_scope"
            assert [c["category"] for c in results[13]["result"]["candidates"]] == [
                "reward_callback"
            ]
            assert results[14]["result"]["time_basis"] == "recalculated_from_snapshot"
            assert results[14]["result"]["records_refreshed"] is False
            assert results[14]["result"]["dataset_as_of"] == results[0]["result"]["dataset_as_of"]
            assert results[15]["result"]["route"] == "clarify_scope"
            assert [c["category"] for c in results[16]["result"]["candidates"]] == ["no_offers"]
            assert results[17]["result"]["route"] == "clarify_scope"
            assert results[17]["result"]["candidates"][0]["category"] == "unknown"
            assert results[17]["result"]["root_cause"] == "unconfirmed"
            empty_date = await session.call_tool("list_accounts", {"as_of": ""})
            assert empty_date.isError
            invalid = await session.call_tool("check_readiness", {"integration_id": "missing"})
            assert invalid.isError
            identifier = await session.call_tool("triage_issue", {"issue_text": "issue_callback"})
            assert identifier.isError
            return {
                "transport": "stdio",
                "model_inference": False,
                "server": init.serverInfo.model_dump(),
                "server_instructions": init.instructions,
                "tool_count": len(tools.tools),
                "prompts": [
                    {"name": name, "response": response.model_dump(mode="json")}
                    for name, response in (
                        ("morning_review", prompt),
                        ("product_feedback_review", feedback_prompt),
                    )
                ],
                "invalid_id_returns_error": True,
                "identifier_input_returns_error": True,
                "empty_review_date_returns_error": True,
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
