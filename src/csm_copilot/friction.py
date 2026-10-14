"""Snapshot of recurring checklist friction, without inferring customer confusion or cause."""

from .brief import cell, text

PRODUCT_QUESTIONS = {
    "currency_approved": "Would a platform-specific approval-status explanation help customers supply the right evidence?",
    "test_only_off": "Would a production-visibility walkthrough help customers confirm the setting?",
    "placement_linked": "Would a placement-to-content example make configuration review easier?",
    "sdk_connected": "Would a connection-sequence example make integration troubleshooting easier?",
    "device_verified": "Would a non-test-device evidence template make validation handoffs clearer?",
    "callback_verified": "Would a callback evidence template clarify the endpoint details needed for review?",
}


def build_friction_digest(engine, include_live: bool = False) -> dict:
    """Aggregate evaluated checks once per integration; never classify absent evidence as failure."""
    accounts = sorted(
        (a for a in engine.data.accounts if include_live or a.stage != "live"),
        key=lambda a: a.id,
    )
    account_ids = {a.id for a in accounts}
    integrations = sorted(
        (i for i in engine.data.integrations if i.account_id in account_ids), key=lambda i: i.id
    )
    themes = {}
    for integration in integrations:
        for check in engine.check_readiness(integration.id)["checks"]:
            theme = themes.setdefault(
                check["id"],
                {
                    "check_id": check["id"],
                    "label": check["label"],
                    "source_url": check["source_url"],
                    "rule_authority": check["authority"],
                    "applicable_integration_ids": [],
                    "members": [],
                },
            )
            if check["status"] == "not_applicable":
                continue
            theme["applicable_integration_ids"].append(integration.id)
            if check["status"] not in ("unknown", "not_met"):
                continue
            theme["members"].append(
                {
                    "account_id": integration.account_id,
                    "account_name": engine.accounts[integration.account_id].name,
                    "integration_id": integration.id,
                    "app": integration.app,
                    "platform": integration.platform,
                    "status": check["status"],
                    "evidence_ids": check["evidence_ids"],
                    "source_records": [
                        engine.evidence[eid].model_dump(mode="json")
                        for eid in check["evidence_ids"]
                    ],
                    "next_question": check["request"],
                }
            )
    results = []
    for theme in themes.values():
        members = theme["members"]
        if not members:
            continue
        affected_accounts = sorted({m["account_id"] for m in members})
        theme.update(
            {
                "affected_account_ids": affected_accounts,
                "affected_account_count": len(affected_accounts),
                "affected_integration_count": len(members),
                "applicable_integration_count": len(theme["applicable_integration_ids"]),
                "unknown_integration_count": sum(m["status"] == "unknown" for m in members),
                "failed_integration_count": sum(m["status"] == "not_met" for m in members),
                "recurring_across_accounts": len(affected_accounts) >= 2,
                "product_question": PRODUCT_QUESTIONS[theme["check_id"]],
                "proposed_owner": "CSM + Product Education (project proposal)",
                "validation_step": "Review the source records, ask affected customers whether the proposed resource addresses their difficulty, and test it before claiming an improvement.",
                "interpretation": "Checklist friction signal; not a confirmed product defect or a measured customer-confusion theme.",
            }
        )
        results.append(theme)
    results.sort(key=lambda t: (-t["affected_account_count"], t["check_id"]))
    return {
        "as_of": engine.data.as_of.isoformat(),
        "synthetic": True,
        "method": "deterministic scoped-check aggregation",
        "include_live": include_live,
        "cohort_account_ids": [a.id for a in accounts],
        "cohort_account_count": len(accounts),
        "cohort_integration_count": len(integrations),
        "themes": results,
        "counting_policy": "One observation per integration and check. Accounts are deduplicated within each theme; themes overlap and their counts must not be added as unique customers. Not-applicable checks are excluded from each theme's denominator.",
        "recurrence_policy": "Recurring means at least two distinct accounts in this snapshot (project policy), not repeated events over time.",
        "boundary": "This is a snapshot of recorded states, not a weekly trend, prevalence estimate, confirmed root cause or product priority score. Proposed questions and owners are unvalidated project suggestions. Nothing was sent to Product.",
    }


def render_friction_brief(digest: dict) -> str:
    lines = [
        "# CSM Copilot — Product feedback review",
        "",
        "> Independent portfolio prototype. Synthetic records. Proposed feedback, not sent.",
        "",
        f"Snapshot: {text(digest['as_of'])}.",
        f"Scope: {digest['cohort_account_count']} accounts / {digest['cohort_integration_count']} integrations; live accounts {'included' if digest['include_live'] else 'excluded'}.",
        "",
        text(digest["counting_policy"]),
        "",
        text(digest["recurrence_policy"]),
    ]
    if not digest["themes"]:
        lines += [
            "",
            "No scoped checklist friction found in the selected cohort. This does not establish that customers have no difficulties.",
        ]
    for theme in digest["themes"]:
        lines += [
            "",
            f"## {text(theme['label'])}",
            "",
            f"{theme['affected_account_count']} distinct accounts; {theme['affected_integration_count']} affected / {theme['applicable_integration_count']} applicable integrations.",
            f"Unknown: {theme['unknown_integration_count']}. Recorded failure: {theme['failed_integration_count']}.",
            "",
            "| Account / integration | State | Source records | Next customer question |",
            "|---|---|---|---|",
        ]
        for member in theme["members"]:
            lines.append(
                f"| {cell(member['account_name'])} / {cell(member['integration_id'])} | {cell(member['status'])} | {cell(', '.join(member['evidence_ids']) or 'No applicable record')} | {cell(member['next_question'])} |"
            )
        lines += [
            "",
            f"**Product question:** {text(theme['product_question'])}",
            f"**Proposed owner:** {text(theme['proposed_owner'])}",
            f"**Validation step:** {text(theme['validation_step'])}",
            f"Related documentation: {theme['source_url']}",
            f"Checklist authority: {text(theme['rule_authority'])}. Product questions are project proposals, not vendor recommendations.",
            "",
            text(theme["interpretation"]),
        ]
        for member in theme["members"]:
            for record in member["source_records"]:
                lines += [
                    "",
                    f"Source {text(record['id'])}, recorded {text(record['at'])}:",
                    "> " + cell(record["text"]),
                ]
    lines += ["", text(digest["boundary"]), ""]
    return "\n".join(lines)
