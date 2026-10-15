"""Check a morning answer against its observed workflow; never certify free prose."""

from typing import Literal, get_args

from pydantic import BaseModel, ConfigDict, Field, StrictBool, ValidationError

from .dependency_policy import MorningReviewPolicy
from .models import CheckID, TicketDetails
from .response_review import PlatformClaim, review_final

FollowupIntent = Literal[
    "evidence_request", "issue_status_review", "launch_plan_review", "post_launch_checkin"
]
HandoffState = Literal["needs_scope", "needs_information", "ready_for_human_review"]


class StrictClaim(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)


class SelectionClaim(StrictClaim):
    account_id: str
    contact_state: Literal["recorded", "unknown"]
    days_since_contact: float | None
    days_to_launch: float | None
    contact_evidence_ids: list[str]


class MorningPlatformClaim(PlatformClaim):
    followup_intent: FollowupIntent


class HandoffClaim(StrictClaim):
    issue_id: str
    integration_id: str
    missing_fields: list[str]
    evidence_ids: list[str]
    handoff_state: HandoffState
    root_cause: str


class MorningClaims(StrictClaim):
    selection: SelectionClaim | None
    platforms: list[MorningPlatformClaim]
    handoffs: list[HandoffClaim]
    nothing_sent: StrictBool
    launch_approved: StrictBool
    explanation: str = Field(min_length=1)


MORNING_FINAL_GUIDANCE = (
    "Host final-answer contract (not customer data): tool work is complete. For this response, "
    'replace the earlier final-string format with one object: {"final":{'
    '"selection":{"account_id":"ID","contact_state":"recorded|unknown",'
    '"days_since_contact":0,"days_to_launch":0,"contact_evidence_ids":["ID"]},'
    '"platforms":[{"integration_id":"ID","decision":"blocked|needs_evidence|checklist_complete",'
    '"unknown_checks":["check_id"],"failed_checks":["check_id"],"evidence_ids":["ID"],'
    '"followup_intent":"evidence_request|issue_status_review|launch_plan_review|post_launch_checkin"}],'
    '"handoffs":[{"issue_id":"ID","integration_id":"ID","missing_fields":["field"],'
    '"evidence_ids":["ID"],"handoff_state":"needs_scope|needs_information|ready_for_human_review",'
    '"root_cause":"state"}],"nothing_sent":true,"launch_approved":false,"explanation":"text"}}. '
    "These are field placeholders, not observed answers. Copy selection values from the first "
    "returned queue account and contact IDs from its context; preserve null for unknown numeric values. "
    "Use selection=null and empty arrays only if the returned queue is empty. Include every selected "
    "integration and recorded issue exactly once. For each platform, unknown_checks means status unknown; "
    "failed_checks means not_met. Use the union of that platform's readiness source IDs, not issue-only IDs. "
    "Copy followup_intent from its English draft. Copy missing fields, evidence IDs, handoff state and "
    "root-cause state from each issue's draft. Use empty arrays when appropriate; never invent IDs. "
    "Explain the selection and platform-specific next actions in at most 220 whitespace-separated words, "
    "with source citations, preserving unknown versus failed checks. State that nothing was sent. "
    "Field matching does not verify your explanation or grant launch approval."
)


def morning_final_schema():
    """Structure and type constraints, with no fixture-specific IDs or expected states."""
    schema = MorningClaims.model_json_schema()
    definitions = schema.pop("$defs", {})
    return {
        "type": "object",
        "properties": {"final": schema},
        "required": ["final"],
        "additionalProperties": False,
        "$defs": definitions,
    }


def _unique_strings(values):
    if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
        raise ValueError("Expected a list of nonempty source identifiers")
    if len(values) != len(set(values)):
        raise ValueError("Duplicate source identifiers in recorded results")
    return values


def _nonempty_text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Required recorded display text is missing")
    return value


def _observations(trace):
    """Replay dependencies; failed calls stay pending and duplicate successes are ambiguous."""
    policy = MorningReviewPolicy()
    queue, context = None, None
    readiness, followups, handoffs = {}, {}, {}
    for step in trace.get("steps", []):
        for call in step.get("tool_calls", []):
            if type(call.get("tool_error")) is not bool:
                raise ValueError("A recorded call must explicitly report its error state")
            action, result = call["action"], call["tool_result"]
            policy.observe(action, result, tool_error=call["tool_error"])
            if call["tool_error"]:
                continue
            name, args = action["tool"], action["arguments"]
            if name == "list_accounts":
                queue = result
            elif name == "get_account_context":
                context = result
            elif name == "check_readiness":
                readiness[args["integration_id"]] = result
            elif name == "draft_followup":
                followups[args["integration_id"]] = result
            elif name == "draft_ticket":
                handoffs[args["issue_id"]] = result
    if queue is None or policy.pending:
        raise ValueError("Required queue, context or scoped tool work is incomplete")
    return queue, context, readiness, followups, handoffs


def review_morning_final(payload, trace):
    """Agreement with unambiguous recorded fields plus a mechanical word limit, not truth."""
    issues = []
    report = {
        "contract": "1-morning-final-fields",
        "status": "rejected",
        "issues": issues,
        "free_text_verification": "not_performed",
        "human_review_required": True,
        "checked_summary": None,
        "boundary": "Matching fields establish agreement with the returned queue, scoped readiness, follow-up purpose and handoff fields only. They do not verify source truth, freshness, the meaning of draft bodies or the model's explanation. The summary is system-rendered from recorded results, not model prose.",
    }
    try:
        claims = MorningClaims.model_validate(payload)
    except ValidationError as exc:
        issues.extend(
            {"field": ".".join(map(str, e["loc"])), "code": "schema", "detail": e["msg"]}
            for e in exc.errors(include_input=False, include_url=False)
        )
        return report
    words = len(claims.explanation.split())
    report["explanation_word_count"] = words
    if not 1 <= words <= 220:
        issues.append(
            {"field": "explanation", "code": "word_limit", "observed": words, "maximum": 220}
        )

    def match(field, observed, expected):
        equal = (
            sorted(observed) == sorted(expected)
            if isinstance(expected, list) and isinstance(observed, list)
            else observed == expected
        )
        if not equal:
            issues.append(
                {"field": field, "code": "mismatch", "expected": expected, "observed": observed}
            )

    try:
        queue, context, readiness, followups, tickets = _observations(trace)
        selected = queue["accounts"][0] if queue["accounts"] else None
        expected_selection = None
        issue_records = {}
        if selected:
            account_id = selected["account_id"]
            _nonempty_text(selected["name"])
            sources = context["evidence"]
            _unique_strings([source["id"] for source in sources])
            source_map = {source["id"]: source for source in sources}

            def source_ids(values, integration_id, kind=None):
                for identifier in _unique_strings(values):
                    source = source_map[identifier]
                    if (
                        source["account_id"] != account_id
                        or source["integration_id"] != integration_id
                    ):
                        raise ValueError("Recorded citation belongs to a different scope")
                    if kind is not None and source["kind"] != kind:
                        raise ValueError("Contact citation must identify a contact record")
                return values

            contacts = source_ids(context["account"]["contact_ids"], None, "contact_record")
            expected_selection = SelectionClaim(
                account_id=account_id,
                contact_state=selected["contact_state"],
                days_since_contact=selected["days_since_contact"],
                days_to_launch=selected["days_to_launch"],
                contact_evidence_ids=contacts,
            ).model_dump()
            for key, ready in readiness.items():
                check_ids = [check["id"] for check in ready["checks"]]
                if len(check_ids) != len(set(check_ids)) or set(check_ids) != set(
                    get_args(CheckID)
                ):
                    raise ValueError("Readiness checks are missing or ambiguous")
                _nonempty_text(ready["app"])
                _nonempty_text(ready["platform"])
                _nonempty_text(followups[key]["next_action"])
                for check in ready["checks"]:
                    if check["status"] not in ("met", "not_met", "unknown", "not_applicable"):
                        raise ValueError("Invalid recorded readiness state")
                    source_ids(check["evidence_ids"], key)
                # Validate the enum without treating the draft's prose as verified.
                MorningPlatformClaim(
                    integration_id=key,
                    decision=ready["decision"],
                    unknown_checks=[],
                    failed_checks=[],
                    evidence_ids=[],
                    followup_intent=followups[key]["intent"],
                )
            issue_records = {issue["id"]: issue for issue in context["issues"]}
            for key, ticket in tickets.items():
                issue = issue_records[key]
                refs = source_ids(ticket["evidence_ids"], issue["integration_id"])
                if refs != [issue["evidence_id"]]:
                    raise ValueError("Handoff citation does not identify the recorded issue source")
                missing = _unique_strings(ticket["missing_fields"])
                if not set(missing) <= set(TicketDetails.model_fields):
                    raise ValueError("Unknown handoff intake field")
                HandoffClaim(
                    issue_id=key,
                    integration_id=issue["integration_id"],
                    missing_fields=missing,
                    evidence_ids=refs,
                    handoff_state=ticket["handoff_state"],
                    root_cause=ticket["root_cause"],
                )
                if ticket["root_cause"] != "unconfirmed":
                    raise ValueError("This workflow does not establish a confirmed root cause")
                _nonempty_text(ticket["next_action"])

        if claims.selection is None or expected_selection is None:
            match(
                "selection",
                claims.selection.model_dump() if claims.selection else None,
                expected_selection,
            )
        else:
            for field, expected in expected_selection.items():
                match("selection." + field, getattr(claims.selection, field), expected)
        base_review = review_final(
            {
                "platforms": [p.model_dump(exclude={"followup_intent"}) for p in claims.platforms],
                "nothing_sent": claims.nothing_sent,
                "launch_approved": claims.launch_approved,
                "explanation": claims.explanation,
            },
            trace,
            tuple(readiness),
        )
        issues.extend(base_review["issues"])
        for platform in claims.platforms:
            if platform.integration_id in followups:
                match(
                    platform.integration_id + ".followup_intent",
                    platform.followup_intent,
                    followups[platform.integration_id]["intent"],
                )
        identifiers = [handoff.issue_id for handoff in claims.handoffs]
        if len(identifiers) != len(set(identifiers)) or set(identifiers) != set(tickets):
            issues.append(
                {
                    "field": "handoffs",
                    "code": "scope",
                    "detail": "Each selected account issue must appear exactly once",
                }
            )
        for handoff in claims.handoffs:
            ticket = tickets.get(handoff.issue_id)
            if ticket is None:
                continue
            expected = {
                "integration_id": issue_records[handoff.issue_id]["integration_id"],
                **{
                    key: ticket[key]
                    for key in ("missing_fields", "evidence_ids", "handoff_state", "root_cause")
                },
            }
            for field, value in expected.items():
                match(handoff.issue_id + "." + field, getattr(handoff, field), value)
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        issues.append(
            {"field": "tool_evidence", "code": "invalid_or_incomplete", "detail": str(exc)}
        )
        return report
    if issues:
        return report
    lines = (
        ["No accounts returned by the snapshot queue."]
        if selected is None
        else [
            f"First account in the returned snapshot queue: {selected['name']} ({selected['account_id']}).",
            f"Contact state: {selected['contact_state']}; days since contact: {selected['days_since_contact']}; days to planned launch: {selected['days_to_launch']}.",
            "Contact sources: "
            + (
                ", ".join(expected_selection["contact_evidence_ids"])
                or "no recorded contact source"
            )
            + ".",
        ]
    )
    lines.append(base_review["checked_summary"])
    for key, ticket in tickets.items():
        lines += [
            f"Issue {key}: {ticket['handoff_state']}; root cause: {ticket['root_cause']}.",
            "Missing intake: " + (", ".join(ticket["missing_fields"]) or "none recorded") + ".",
            "Issue sources: " + ", ".join(ticket["evidence_ids"]) + ".",
            "Proposed next action: " + ticket["next_action"],
        ]
    report["status"] = "structured_fields_match"
    report["checked_summary"] = "\n".join(lines)
    return report
