"""Small, inspectable model-to-tool protocol used only by the optional local host."""

import json


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"Non-JSON numeric constant: {value}")


def parse_action(raw: str, allowed_tools: set[str]) -> dict:
    """Accept one exact JSON action; reject ambiguous, extra or executable instructions."""
    action = json.loads(raw, object_pairs_hook=unique_keys, parse_constant=reject_constant)
    if not isinstance(action, dict):
        raise ValueError("Expected one JSON object")
    if set(action) == {"final"} and isinstance(action["final"], str) and action["final"].strip():
        return action
    if set(action) != {"tool", "arguments"}:
        raise ValueError("Use exactly tool + arguments, or final")
    if not isinstance(action["tool"], str) or action["tool"] not in allowed_tools:
        raise ValueError("Tool is not in the discovered read-only allowlist")
    if not isinstance(action["arguments"], dict):
        raise ValueError("Tool arguments must be an object")
    return action


def parse_actions(raw: str, allowed_tools: set[str]) -> list[dict]:
    """Accept one action or an explicit bounded array; validate all before execution."""
    value = json.loads(raw, object_pairs_hook=unique_keys, parse_constant=reject_constant)
    batch = value if isinstance(value, list) else [value]
    if not 1 <= len(batch) <= 4:
        raise ValueError("An action batch must contain 1..4 actions")
    actions = [parse_action(json.dumps(item), allowed_tools) for item in batch]
    if len(actions) > 1 and any("final" in action for action in actions):
        raise ValueError("Final must be a separate response after tool results")
    return actions


def trace_coverage(trace: dict) -> dict:
    """Check requested actions were observed; this is not semantic grading of final prose."""
    calls = [call for step in trace.get("steps", []) for call in step.get("tool_calls", [step])]
    successful = [call for call in calls if "tool_result" in call and not call.get("tool_error")]
    required = {
        "android_readiness": ("check_readiness", "lantern_android"),
        "ios_readiness": ("check_readiness", "lantern_ios"),
        "android_followup": ("draft_followup", "lantern_android"),
        "ios_followup": ("draft_followup", "lantern_ios"),
    }
    checks = {
        label: any(
            step["action"]["tool"] == tool
            and step["action"]["arguments"].get("integration_id") == integration
            and (tool != "draft_followup" or step["action"]["arguments"].get("lang", "en") == "en")
            for step in successful
        )
        for label, (tool, integration) in required.items()
    }
    return {
        "checks": checks,
        "observed": sum(checks.values()),
        "required": len(checks),
        "final_response_present": bool(trace.get("final")),
        "boundary": "Tool coverage only. Does not establish that the final response is faithful, useful or complete.",
    }
