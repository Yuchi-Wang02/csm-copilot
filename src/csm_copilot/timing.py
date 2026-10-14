"""Describe the dates of scoped supporting records without imposing an expiry policy."""

from datetime import datetime


def evidence_timing(readiness: dict, context: dict) -> dict:
    as_of = datetime.fromisoformat(readiness["as_of"])
    if as_of.tzinfo is None:
        raise ValueError("Evidence timing requires a timezone-aware snapshot")
    records = {}
    for record in context["evidence"]:
        if (
            record["account_id"] == context["account"]["id"]
            and record["integration_id"] == readiness["integration_id"]
        ):
            records.setdefault(record["id"], []).append(record)
    included = {}
    unavailable = set()
    for check in readiness["checks"]:
        for identifier in check["evidence_ids"]:
            matches = records.get(identifier, [])
            if len(matches) != 1:
                unavailable.add(identifier)
                continue
            record = matches[0]
            recorded_at = datetime.fromisoformat(record["at"])
            if recorded_at.tzinfo is None or recorded_at > as_of:
                raise ValueError(
                    "Evidence timing requires an aware timestamp at or before snapshot"
                )
            item = included.setdefault(
                identifier,
                {
                    "id": identifier,
                    "kind": record["kind"],
                    "recorded_at": record["at"],
                    "age_days": round((as_of - recorded_at).total_seconds() / 86400, 2),
                    "check_ids": [],
                },
            )
            if check["id"] not in item["check_ids"]:
                item["check_ids"].append(check["id"])
    return {
        "as_of": readiness["as_of"],
        "integration_id": readiness["integration_id"],
        "records": sorted(
            included.values(),
            key=lambda item: (datetime.fromisoformat(item["recorded_at"]), item["id"]),
        ),
        "unavailable_ids": sorted(unavailable),
        "boundary": "Age is elapsed time at the fixed snapshot, rounded to two decimals. It does not expire evidence, change readiness or prove that a report is still current. Review whether a fresh confirmation or test is needed.",
    }
