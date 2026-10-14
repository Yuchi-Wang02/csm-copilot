"""A compact first-run view of the original workflow snapshot."""


def _text(value):
    """Keep record values on one terminal line, without control characters."""
    return " ".join("".join(c if c.isprintable() else " " for c in str(value)).split())


def render_summary(workflow: dict) -> str:
    """Summarize existing results without updating evidence or contact history."""
    packets = workflow["packets"]
    lines = [
        "CSM Copilot - morning review",
        f"Snapshot: {_text(workflow['as_of'])}",
        "Synthetic data | deterministic replay | no model inference | nothing sent",
        f"Queue: {len(packets)} accounts, {sum(len(p['integrations']) for p in packets)} platforms.",
        "Order: planned launch date. Original snapshot; comparison updates are excluded.",
    ]
    if not packets:
        lines += ["", "No accounts in this review queue."]
    for number, packet in enumerate(packets, 1):
        selection = packet["selection"]
        age = selection["days_since_contact"]
        age_text = "unknown" if age is None else f"{age:g} days ago"
        lines += [
            "",
            f"{number}. {_text(selection['name'])} ({_text(selection['account_id'])})",
            f"   Last contact: {age_text}; planned launch: {_text(packet['context']['account']['target_launch'])}",
        ]
        for item in packet["integrations"]:
            ready = item["readiness"]
            lines.append(
                f"   {_text(ready['app'])} / {_text(ready['platform'])}: {_text(ready['decision'])}"
            )
            for check in ready["checks"]:
                if check["status"] in ("unknown", "not_met"):
                    sources = ", ".join(check["evidence_ids"]) or "no applicable record"
                    lines.append(
                        f"     {_text(check['id'])}: {_text(check['status'])} [{_text(sources)}]"
                    )
            lines.append(f"     Next: {_text(item['followup_en']['next_action'])}")
            for issue in packet["context"]["issues"]:
                if issue["integration_id"] != ready["integration_id"]:
                    continue
                matches = [t for t in packet["tickets"] if t["draft_id"] == f"ticket-{issue['id']}"]
                if not matches:
                    lines.append(f"     {_text(issue['id'])}: no handoff draft in this packet")
                    continue
                if len(matches) != 1:
                    lines.append(
                        f"     {_text(issue['id'])}: handoff unavailable; {len(matches)} matching drafts. Review the packet."
                    )
                    continue
                ticket = matches[0]
                if ticket["handoff_state"] == "needs_scope":
                    lines += [
                        f"     Handoff {_text(issue['id'])}: needs_scope",
                        "     Scope first: generic field completeness does not establish the request.",
                        f"     Next for this issue: {_text(ticket['next_action'])}",
                    ]
                else:
                    missing = ", ".join(ticket["missing_fields"]) or "none"
                    lines.append(
                        f"     Handoff {_text(issue['id'])}: {_text(ticket['handoff_state'])}; missing: {_text(missing)}"
                    )
                lines.append(f"     Proposed owner: {_text(ticket['suggested_owner'])}")
    lines += [
        "",
        "Checklist completion is not launch approval or issue resolution.",
        "For full drafts and evidence, run: csm-demo --format markdown --output morning-review.md",
    ]
    return "\n".join(lines) + "\n"
