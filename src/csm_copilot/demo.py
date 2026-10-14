"""Reproducible workflow replay; deliberately does not masquerade as an LLM run."""

import argparse
import json
from pathlib import Path

from .engine import Copilot
from .models import Dataset


def build_demo():
    engine = Copilot()
    selection = engine.list_accounts()
    packets = []
    for selected in selection["accounts"]:
        context = engine.get_account_context(selected["account_id"])
        integrations = []
        for i in context["integrations"]:
            integrations.append(
                {
                    "readiness": engine.check_readiness(i["id"]),
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
            "at": updated["as_of"],
            "kind": "customer_report",
            "text": "Synthetic update: Android currency is approved and Test Only is off. No new device test yet.",
        }
    )
    for i in updated["integrations"]:
        if i["id"] == "lantern_android":
            for key in ("currency_approved", "test_only_off"):
                i["facts"][key] = {"status": "met", "evidence_ids": ["reply_android_settings"]}
    after = Copilot(Dataset.model_validate(updated)).check_readiness("lantern_android")
    return {
        "project": "CSM Copilot",
        "synthetic": True,
        "as_of": selection["as_of"],
        "execution_mode": "deterministic workflow replay; no model inference",
        "selection": selection,
        "packets": packets,
        "counterfactual": {
            "description": "Customer confirms two Android settings; no fresh device test.",
            "before": engine.check_readiness("lantern_android"),
            "after": after,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="Write JSON; default prints to stdout")
    args = parser.parse_args()
    content = json.dumps(build_demo(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content)


if __name__ == "__main__":
    main()
