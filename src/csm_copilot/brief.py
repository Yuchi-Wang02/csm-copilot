"""Human-readable export of the same review packet used by the static explorer."""

import html
import re
from copy import deepcopy

from .timing import evidence_timing

INTENTS = {
    "evidence_request": "Collect evidence",
    "issue_status_review": "Confirm the recorded issue's current status",
    "launch_plan_review": "Review the launch plan",
    "post_launch_checkin": "Check the live experience",
}


def text(value):
    """Keep customer strings as text in Markdown, including raw HTML and table delimiters."""
    escaped = html.escape(str(value), quote=False)
    return re.sub(r"([\\`*_{}\[\]()#+!|])", r"\\\1", escaped)


def cell(value):
    return text(value).replace("\r\n", "\n").replace("\r", "\n").replace("\n", " / ")


def _issue_source(packet, ticket):
    """Resolve the original record in the current account and issue's platform."""
    issues = [i for i in packet["context"]["issues"] if "ticket-" + i["id"] == ticket["draft_id"]]
    if len(issues) != 1:
        return None
    issue = issues[0]
    sources = [
        record
        for record in packet["context"]["evidence"]
        if record["id"] == issue["evidence_id"]
        and record["account_id"] == packet["context"]["account"]["id"]
        and record["integration_id"] == issue["integration_id"]
    ]
    return sources[0] if len(sources) == 1 else None


def _case_packet(workflow: dict, integration_id: str) -> dict:
    matches = [
        (packet, item)
        for packet in workflow["packets"]
        for item in packet["integrations"]
        if item["readiness"]["integration_id"] == integration_id
    ]
    if len(matches) != 1:
        raise ValueError("integration_id must identify exactly one platform in the review queue")
    original, item = matches[0]
    packet = deepcopy(original)
    packet["integrations"] = [deepcopy(item)]
    packet["selection"]["integration_ids"] = [integration_id]
    context = packet["context"]
    context["integrations"] = [i for i in context["integrations"] if i["id"] == integration_id]
    context["issues"] = [i for i in context["issues"] if i["integration_id"] == integration_id]
    ticket_ids = {f"ticket-{issue['id']}" for issue in context["issues"]}
    packet["tickets"] = [t for t in packet["tickets"] if t["draft_id"] in ticket_ids]
    context["evidence"] = [
        record
        for record in context["evidence"]
        if record["account_id"] == context["account"]["id"]
        and record["integration_id"] in (None, integration_id)
    ]
    return packet


def render_review_brief(workflow: dict, lang: str = "en", integration_id: str | None = None) -> str:
    """Export synthetic findings and drafts; do not rerun or mutate the workflow."""
    if lang not in ("en", "zh"):
        raise ValueError("lang must be en or zh")
    packets = (
        [_case_packet(workflow, integration_id)]
        if integration_id is not None
        else workflow["packets"]
    )
    lines = [
        "# CSM Copilot — "
        + ("Platform review brief" if integration_id is not None else "Morning review brief"),
        "",
        "> Independent portfolio prototype. All customer records are synthetic. Nothing was sent or submitted.",
        "",
        f"Snapshot: **{text(workflow['as_of'])}**",
        f"Execution: {text(workflow['execution_mode'])}.",
        f"Client draft language: {'English' if lang == 'en' else 'Chinese'}.",
        "",
    ]
    if integration_id is not None:
        lines += [
            f"Scope: **{text(integration_id)}**. Original snapshot only; the separate synthetic-update comparison is excluded. Other platforms and accounts are excluded; account contact records are retained.",
            "",
        ]
    lines += [
        "## Selected platform" if integration_id is not None else "## Today's review queue",
        "",
        "Selection: strictly more than three days since actual contact; missing contact history is included as unknown. Live accounts are excluded from this bundled morning queue.",
        "",
        "| Account | Days since contact | Planned launch | Included integrations |"
        if integration_id is not None
        else "| Account | Days since contact | Planned launch | Integrations |",
        "|---|---:|---|---|",
    ]
    for packet in packets:
        account = packet["context"]["account"]
        age = packet["selection"]["days_since_contact"]
        lines.append(
            f"| {cell(account['name'])} ({cell(account['id'])}) | {age if age is not None else 'Unknown'} | {cell(account['target_launch'])} | {len(packet['integrations'])} |"
        )
    lines += [
        "",
        "Priority is the planned launch date, not a predicted risk or revenue score. All next steps are proposals for CSM review; no deadline or customer agreement is inferred.",
    ]
    for packet in packets:
        account = packet["context"]["account"]
        lines += [
            "",
            f"## {text(account['name'])} — {text(account['id'])}",
            "",
            f"Recorded stage: {text(account['stage'])}. Last actual contact: {text(packet['selection']['last_contact'] or 'Unknown')}.",
        ]
        for item in packet["integrations"]:
            ready = item["readiness"]
            draft = item[f"followup_{lang}"]
            lines += [
                "",
                f"### {text(ready['app'])} / {text(ready['platform'])}",
                "",
                f"**Scoped readiness:** {text(ready['decision'])}.",
                f"**Follow-up purpose:** {INTENTS[draft['intent']]}. **Proposed owner:** CSM.",
                f"**Next action:** {text(draft['next_action'])}",
                "",
                "| Check | State | Source record IDs |",
                "|---|---|---|",
            ]
            for check in ready["checks"]:
                lines.append(
                    f"| {cell(check['label'])} | {cell(check['status'])} | {cell(', '.join(check['evidence_ids']) or 'No applicable record')} |"
                )
            timing = evidence_timing(ready, packet["context"])
            lines += [
                "",
                "**Timing of supporting records** (oldest first)",
                "",
                "| Record | Source type | Recorded at | Days before snapshot | Supports |",
                "|---|---|---|---:|---|",
            ]
            for record in timing["records"]:
                lines.append(
                    f"| {cell(record['id'])} | {cell(record['kind'])} | {cell(record['recorded_at'])} | {record['age_days']:.2f} | {cell(', '.join(record['check_ids']))} |"
                )
            if not timing["records"]:
                lines += ["", "No available supporting records for this scoped checklist."]
            if timing["unavailable_ids"]:
                lines += [
                    "",
                    "Unavailable scoped sources: " + text(", ".join(timing["unavailable_ids"])),
                ]
            lines += ["", timing["boundary"]]
            lines += [
                "",
                text(ready["boundary"]),
                "",
                "**Customer follow-up draft — not sent**",
                "",
            ]
            lines += ["> " + text(line) for line in draft["body"].splitlines()]
            lines += [
                "",
                f"Draft evidence: {text(', '.join(draft['evidence_ids']) or 'No evidence records')}. Contact history unchanged.",
            ]
        if integration_id is not None and not packet["context"]["issues"]:
            lines += [
                "",
                "**Recorded issues:** None for this platform in the snapshot. This does not establish that no issue exists or that a previous issue was resolved.",
            ]
        for ticket in packet["tickets"]:
            lines += [
                "",
                f"### Technical handoff — {text(ticket['draft_id'])}",
                "",
                f"**{text(ticket['title'])}**",
                "",
                f"Handoff state: {text(ticket['handoff_state'])}. Root cause: {text(ticket['root_cause'])}.",
                f"Suggested owner: {text(ticket['suggested_owner'])}.",
                "",
                "| Known field | Value | Source record |",
                "|---|---|---|",
            ]
            for key, value in ticket["fields"].items():
                lines.append(
                    f"| {cell(key)} | {cell(value)} | {cell(ticket['field_sources'][key]['source_id'])} |"
                )
            lines += [
                "",
                "**Missing information:** "
                + (
                    text(", ".join(ticket["missing_fields"]))
                    if ticket["missing_fields"]
                    else "None in the scoped required fields; human review is still required."
                ),
                "",
                f"**Next action:** {text(ticket['next_action'])}",
            ]
            if ticket.get("collection_requests"):
                lines += ["", "**Request missing intake details**", ""]
                lines += [
                    "- " + cell(request["request"]) for request in ticket["collection_requests"]
                ]
            if ticket.get("collection_boundary"):
                lines += ["", text(ticket["collection_boundary"])]
            lines += ["", "**Original issue record**", ""]
            source = _issue_source(packet, ticket)
            if source is None:
                lines += [
                    "Original issue record unavailable for this platform. Review the source before using the copied handoff text."
                ]
            else:
                label = {"customer_report": "Customer report", "test_record": "Test record"}.get(
                    source.get("kind"), "Source type unavailable"
                )
                lines += [f"Source type: {label}. Recorded at: {text(source['at'])}.", ""]
                lines += ["> " + text(line) for line in source["text"].splitlines()]
            lines += [
                "",
                "Source record: " + text(", ".join(ticket["evidence_ids"])),
                "",
                "**Questions to review before handoff**",
                "",
                "Suggested questions from lexical triage. Review what is already known before asking the customer; these do not establish a root cause.",
            ]
            for candidate in ticket["triage"]["candidates"]:
                label = (
                    "Clarify the request"
                    if candidate["category"] == "unknown"
                    else "Candidate: " + candidate["category"].replace("_", " ")
                )
                lines += ["", f"**{text(label)}**", ""]
                lines += ["- " + cell(question) for question in candidate["questions"]]
                if candidate["source_url"]:
                    lines += ["", "Related documentation: " + text(candidate["source_url"])]
            lines += ["", *[text(note) for note in ticket["triage"]["notes"]]]
    lines += [
        "",
        "## Evidence index",
        "",
        "These are declared synthetic source records, not independent verification. Structured claims must match account, integration and checklist scope.",
        "",
        "| Record | Account / integration | Recorded at | Source text |",
        "|---|---|---|---|",
    ]
    for packet in packets:
        for record in packet["context"]["evidence"]:
            scope = record["account_id"] + " / " + (record["integration_id"] or "account contact")
            lines.append(
                f"| {cell(record['id'])} | {cell(scope)} | {cell(record['at'])} | {cell(record['text'])} |"
            )
    sources = sorted(
        {
            check["source_url"]
            for p in packets
            for i in p["integrations"]
            for check in i["readiness"]["checks"]
        }
    )
    lines += ["", "## Product sources and review boundaries", ""]
    # URLs originate in the bundled rule register, never in arbitrary customer messages.
    lines += [f"- {url}" for url in sources]
    lines += [
        "",
        "The rule register distinguishes official product documentation from project operating policies. Checklist completion is not vendor launch approval. Triage candidates are not confirmed root causes. Promise-pattern lint does not verify arbitrary model-written claims.",
        "",
        "This export is a deterministic review artifact, not evidence of a live model run, independent human validation, customer impact or actual outreach.",
        "",
    ]
    return "\n".join(lines)
