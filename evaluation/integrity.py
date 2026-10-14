"""Replay small, labeled data-integrity probes; not an AI accuracy benchmark."""

import copy
import json
from pathlib import Path

from pydantic import ValidationError

from csm_copilot.engine import Copilot
from csm_copilot.models import Dataset

ROOT = Path(__file__).resolve().parents[1]


def build_integrity_report():
    baseline = Copilot().data.model_dump(mode="json")
    specs = [
        {
            "id": "valid_same_platform",
            "label": "Keep correctly scoped evidence",
            "change": "Use the existing Android device-failure record for its Android device check.",
            "reason": "Valid provenance is accepted even when the business result is a blocker.",
            "expected": "accepted",
        },
        {
            "id": "cross_platform",
            "label": "Reuse an iOS pass for Android",
            "change": "Set Android currency approval to met using lantern_ios_currency_approved.",
            "reason": "A real source ID is insufficient when it describes another platform.",
            "expected": "rejected",
        },
        {
            "id": "wrong_check",
            "label": "Use a connection test to prove approval",
            "change": "Set Android currency approval to met using lantern_android_sdk_connected.",
            "reason": "The app matches, but SDK connection does not establish currency approval.",
            "expected": "rejected",
        },
        {
            "id": "other_customer_contact",
            "label": "Borrow another customer's contact",
            "change": "Replace Lantern's last-contact reference with contact_acc_011 from Orbit.",
            "reason": "Another customer's recent contact must not remove Lantern from the follow-up queue.",
            "expected": "rejected",
        },
        {
            "id": "ticket_identity",
            "label": "Overwrite the handoff platform",
            "change": "Insert platform: iOS into the Android issue's free-form details.",
            "reason": "App and platform come from the validated integration, not ticket detail fields.",
            "expected": "rejected",
        },
        {
            "id": "reversed_claim",
            "label": "Turn a recorded failure into a pass",
            "change": "Change the Android device-check fact to met, leaving its not_met source claim intact.",
            "reason": "Matching source ownership does not permit reversing what the source asserts.",
            "expected": "rejected",
        },
        {
            "id": "conflicting_reports",
            "label": "Keep disagreement visible",
            "change": "Add a contrary Android customer report and retain both records under an unknown device-check state.",
            "reason": "The schema accepts explicit uncertainty; it does not decide which report is true.",
            "expected": "accepted",
        },
        {
            "id": "empty_detail",
            "label": "Treat a blank SDK version as missing",
            "change": "Set the SDK version to whitespace only.",
            "reason": "Whitespace cannot satisfy the engineering handoff's required information.",
            "expected": "accepted",
        },
    ]
    rows = []
    for spec in specs:
        data = copy.deepcopy(baseline)
        facts = data["integrations"][0]["facts"]
        case = spec["id"]
        if case == "cross_platform":
            facts["currency_approved"] = {
                "status": "met",
                "evidence_ids": ["lantern_ios_currency_approved"],
            }
        elif case == "wrong_check":
            facts["currency_approved"] = {
                "status": "met",
                "evidence_ids": ["lantern_android_sdk_connected"],
            }
        elif case == "other_customer_contact":
            data["accounts"][0]["contact_ids"] = ["contact_acc_011"]
        elif case == "ticket_identity":
            data["issues"][0]["details"]["platform"] = "iOS"
        elif case == "reversed_claim":
            facts["device_verified"]["status"] = "met"
        elif case == "conflicting_reports":
            data["evidence"].append(
                {
                    "id": "contrary_customer_report",
                    "account_id": "acc_014",
                    "integration_id": "lantern_android",
                    "at": data["as_of"],
                    "kind": "customer_report",
                    "text": "Synthetic report: the Android device now works.",
                    "claims": {"device_verified": "met"},
                }
            )
            facts["device_verified"] = {
                "status": "unknown",
                "evidence_ids": ["lantern_android_device_verified", "contrary_customer_report"],
            }
        elif case == "empty_detail":
            data["issues"][0]["details"]["sdk_version"] = " \t "
        try:
            engine = Copilot(Dataset.model_validate(data))
            observed = "accepted"
            result = {
                "readiness": engine.check_readiness("lantern_android")["decision"],
                "device_check": engine.integrations["lantern_android"]
                .facts["device_verified"]
                .status,
                "ticket_missing_fields": engine.draft_ticket("issue_blank")["missing_fields"],
            }
        except ValidationError as exc:
            observed = "rejected"
            result = {
                "errors": [{"location": list(e["loc"]), "message": e["msg"]} for e in exc.errors()]
            }
        rows.append(
            {
                **spec,
                "observed": observed,
                "matches_expectation": observed == spec["expected"],
                "result": result,
            }
        )
    return {
        "execution_mode": "schema validation replay; no model inference",
        "scope": "Eight developer-authored mutations of the synthetic fixture, not a general safety benchmark.",
        "semantic_boundary": "Checks declared scope and structured claims; does not verify source text or external truth.",
        "cases": rows,
    }


def write_report():
    report = build_integrity_report()
    (ROOT / "evidence/integrity.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report


if __name__ == "__main__":
    result = write_report()
    print(
        f"{sum(r['matches_expectation'] for r in result['cases'])}/{len(result['cases'])} integrity probes matched their expected acceptance state."
    )
