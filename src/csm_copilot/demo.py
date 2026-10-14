"""Reproducible workflow replay; deliberately does not masquerade as an LLM run."""

import argparse
import json
import sys
from pathlib import Path

from .brief import render_review_brief
from .engine import Copilot
from .models import Dataset
from .summary import render_summary
from .timing import evidence_timing


def build_demo():
    engine = Copilot()
    selection = engine.list_accounts()
    packets = []
    for selected in selection["accounts"]:
        context = engine.get_account_context(selected["account_id"])
        integrations = []
        for i in context["integrations"]:
            readiness = engine.check_readiness(i["id"])
            integrations.append(
                {
                    "readiness": readiness,
                    "evidence_timing": evidence_timing(readiness, context),
                    "followup_en": engine.draft_followup(i["id"], "en"),
                    "followup_zh": engine.draft_followup(i["id"], "zh"),
                }
            )
        packets.append(
            {
                "selection": selected,
                "context": context,
                "integrations": integrations,
                "tickets": [engine.draft_ticket(x["id"]) for x in context["issues"]],
            }
        )
    # Counterfactual fixture: two new confirmations do not prove a new device test passed.
    updated = engine.data.model_dump(mode="json")
    updated["evidence"].append(
        {
            "id": "reply_android_settings",
            "account_id": "acc_014",
            "integration_id": "lantern_android",
            "at": updated["as_of"],
            "kind": "customer_report",
            "claims": {"currency_approved": "met", "test_only_off": "met"},
            "text": "Synthetic update: Android currency is approved and Test Only is off. No new device test yet.",
        }
    )
    for i in updated["integrations"]:
        if i["id"] == "lantern_android":
            for key in ("currency_approved", "test_only_off"):
                i["facts"][key] = {"status": "met", "evidence_ids": ["reply_android_settings"]}
    after_engine = Copilot(Dataset.model_validate(updated))
    after = after_engine.check_readiness("lantern_android")
    before = engine.check_readiness("lantern_android")
    # A later test record changes the checklist, not the status of the earlier issue.
    verified_data = after_engine.data.model_dump(mode="json")
    verified_data["evidence"].append(
        {
            "id": "fresh_android_checks",
            "account_id": "acc_014",
            "integration_id": "lantern_android",
            "at": verified_data["as_of"],
            "kind": "test_record",
            "claims": {"device_verified": "met", "callback_verified": "met"},
            "text": "Synthetic test: device and callback checks passed. The earlier customer issue has not been reconfirmed.",
        }
    )
    for item in verified_data["integrations"]:
        if item["id"] == "lantern_android":
            for key in ("device_verified", "callback_verified"):
                item["facts"][key] = {"status": "met", "evidence_ids": ["fresh_android_checks"]}
    verified_engine = Copilot(Dataset.model_validate(verified_data))
    verified = verified_engine.check_readiness("lantern_android")
    return {
        "project": "CSM Copilot",
        "synthetic": True,
        "as_of": selection["as_of"],
        "execution_mode": "deterministic workflow replay; no model inference",
        "selection": selection,
        "packets": packets,
        "counterfactual": {
            "description": "Customer confirms two Android settings; no fresh device test.",
            "before": before,
            "after": after,
            "before_timing": evidence_timing(before, engine.get_account_context("acc_014")),
            "after_timing": evidence_timing(after, after_engine.get_account_context("acc_014")),
            "verified": verified,
            "verified_timing": evidence_timing(
                verified, verified_engine.get_account_context("acc_014")
            ),
            "verified_followup": verified_engine.draft_followup("lantern_android", "en"),
            "verified_context": verified_engine.get_account_context("acc_014"),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="Write the export; default prints to stdout")
    parser.add_argument("--format", choices=("json", "markdown", "summary"), default="json")
    parser.add_argument(
        "--integration",
        help="Export one platform from the review queue; requires --format markdown",
    )
    parser.add_argument(
        "--lang",
        choices=("en", "zh"),
        default="en",
        help="Client draft language for the Markdown export; JSON always includes both",
    )
    args = parser.parse_args()
    if args.integration is not None and args.format != "markdown":
        parser.error("--integration requires --format markdown; JSON preserves the full workflow")
    if args.format == "summary" and args.lang != "en":
        parser.error(
            "--format summary is English; use --format markdown --lang zh for Chinese drafts"
        )
    workflow = build_demo()
    try:
        if args.format == "markdown":
            content = render_review_brief(workflow, args.lang, args.integration)
        elif args.format == "summary":
            content = render_summary(workflow)
        else:
            content = json.dumps(workflow, ensure_ascii=False, indent=2) + "\n"
    except ValueError as exc:
        parser.error(str(exc))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8", newline="\n")
    else:
        sys.stdout.buffer.write(content.encode("utf-8"))


if __name__ == "__main__":
    main()
