"""Check model-declared fields against observed tool results, not against external truth."""

import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, StrictBool, ValidationError

from .host_protocol import parse_actions, reject_constant, unique_keys
from .models import CheckID

REQUIRED_INTEGRATIONS = ("lantern_android", "lantern_ios")


class PlatformClaim(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    integration_id: str
    decision: Literal["blocked", "needs_evidence", "checklist_complete"]
    unknown_checks: list[CheckID]
    failed_checks: list[CheckID]
    evidence_ids: list[str]


class FinalClaims(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    platforms: list[PlatformClaim]
    nothing_sent: StrictBool
    launch_approved: StrictBool
    explanation: str


def final_response_schema() -> dict:
    """Constrain structure and field types, never the observed account answers."""
    schema = FinalClaims.model_json_schema()
    definitions = schema.pop("$defs", {})
    return {
        "type": "object",
        "properties": {"final": schema},
        "required": ["final"],
        "additionalProperties": False,
        "$defs": definitions,
    }


def parse_grounded_actions(raw: str, allowed_tools: set[str]) -> list[dict]:
    value = json.loads(raw, object_pairs_hook=unique_keys, parse_constant=reject_constant)
    if isinstance(value, dict) and set(value) == {"final"}:
        # Preserve invalid final payloads so the field review can explain rejection.
        return [value]
    return parse_actions(raw, allowed_tools)


def observed_results(trace: dict, required_integrations=REQUIRED_INTEGRATIONS) -> dict:
    """Only successful calls actually present in this trace can support the final response."""
    result = {key: {"readiness": None, "followup": None} for key in required_integrations}
    for step in trace.get("steps", []):
        for call in step.get("tool_calls", [step]):
            if "tool_result" not in call or call.get("tool_error"):
                continue
            action = call["action"]
            key = action["arguments"].get("integration_id")
            if key not in result:
                continue
            if action["tool"] == "check_readiness":
                result[key]["readiness"] = call["tool_result"]
            elif (
                action["tool"] == "draft_followup" and action["arguments"].get("lang", "en") == "en"
            ):
                result[key]["followup"] = call["tool_result"]
    return result


def review_final(payload, trace: dict, required_integrations=REQUIRED_INTEGRATIONS) -> dict:
    """Exact field matching only; deliberately makes no entailment claim about explanation."""
    issues = []
    result = {
        "status": "rejected",
        "issues": issues,
        "free_text_verification": "not_performed",
        "human_review_required": True,
        "checked_summary": None,
        "boundary": "Matching fields prove agreement with recorded tool results only. They do not verify source truth, freshness, compliance or the model's free-form explanation.",
    }
    try:
        claims = FinalClaims.model_validate(payload)
    except ValidationError as exc:
        issues.extend(
            {"field": ".".join(map(str, e["loc"])), "code": "schema", "detail": e["msg"]}
            for e in exc.errors(include_input=False, include_url=False)
        )
        return result
    keys = [p.integration_id for p in claims.platforms]
    if len(keys) != len(set(keys)) or set(keys) != set(required_integrations):
        issues.append(
            {
                "field": "platforms",
                "code": "scope",
                "detail": "Each required integration must appear exactly once; no extra integrations.",
            }
        )
    observed = observed_results(trace, required_integrations)
    for key, values in observed.items():
        if values["readiness"] is None or values["followup"] is None:
            issues.append(
                {
                    "field": key,
                    "code": "missing_tool_evidence",
                    "detail": "Readiness and an English follow-up must both be observed before final review.",
                }
            )
    if not claims.nothing_sent:
        issues.append(
            {
                "field": "nothing_sent",
                "code": "boundary",
                "detail": "This read-only workflow sends nothing.",
            }
        )
    if claims.launch_approved:
        issues.append(
            {
                "field": "launch_approved",
                "code": "boundary",
                "detail": "Scoped checklist completion cannot approve launch.",
            }
        )
    for claim in claims.platforms:
        values = observed.get(claim.integration_id)
        if not values or values["readiness"] is None or values["followup"] is None:
            continue
        ready, draft = values["readiness"], values["followup"]
        if draft.get("sent") is not False or draft.get("contact_history_changed") is not False:
            issues.append(
                {
                    "field": claim.integration_id,
                    "code": "unexpected_tool_state",
                    "detail": "Follow-up result does not establish a read-only draft.",
                }
            )
        expected = {
            "decision": ready["decision"],
            "unknown_checks": sorted(c["id"] for c in ready["checks"] if c["status"] == "unknown"),
            "failed_checks": sorted(c["id"] for c in ready["checks"] if c["status"] == "not_met"),
            "evidence_ids": sorted({eid for c in ready["checks"] for eid in c["evidence_ids"]}),
        }
        for field, target in expected.items():
            value = getattr(claim, field)
            if (sorted(value) if isinstance(value, list) else value) != target:
                issues.append(
                    {
                        "field": f"{claim.integration_id}.{field}",
                        "code": "mismatch",
                        "expected": target,
                        "observed": value,
                    }
                )
    if issues:
        return result
    lines = []
    for key in required_integrations:
        ready = observed[key]["readiness"]
        lines += [f"{ready['app']} / {ready['platform']}: {ready['decision']}."]
        for check in ready["checks"]:
            refs = ", ".join(check["evidence_ids"]) or "no applicable record"
            lines += [f"- {check['label']}: {check['status']} [{refs}]."]
        lines += [f"Proposed next action: {observed[key]['followup']['next_action']}"]
    lines += ["Nothing was sent. This scoped checklist does not grant launch approval."]
    result["status"] = "structured_fields_match"
    result["checked_summary"] = "\n".join(lines)
    return result
