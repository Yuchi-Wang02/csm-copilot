"""Validate fixture boundaries before any tool uses customer evidence."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Status = Literal["met", "not_met", "unknown", "not_applicable"]
CheckID = Literal[
    "currency_approved",
    "test_only_off",
    "placement_linked",
    "sdk_connected",
    "device_verified",
    "callback_verified",
]


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Evidence(Record):
    id: str
    account_id: str
    integration_id: str | None = None
    at: datetime
    kind: Literal["customer_report", "test_record", "sales_handoff", "contact_record"]
    text: str
    language: Literal["en", "zh"] = "en"
    claims: dict[CheckID, Literal["met", "not_met"]] = Field(default_factory=dict)


class Fact(Record):
    status: Status
    evidence_ids: list[str] = Field(default_factory=list)


class Integration(Record):
    id: str
    account_id: str
    app: str
    platform: Literal["Android", "iOS"]
    currency_mode: Literal["self_managed", "tapjoy_managed"]
    facts: dict[CheckID, Fact]


class Account(Record):
    id: str
    name: str
    stage: Literal["integration", "validation", "live"]
    target_launch: datetime
    contact_ids: list[str]


class TicketDetails(Record):
    """Only evidence-collection fields; identity comes from the integration record."""

    sdk_version: str | None = None
    region: str | None = None
    time_window: str | None = None
    reproduction_steps: str | None = None
    redacted_logs: str | None = None

    @field_validator("*")
    @classmethod
    def empty_means_missing(cls, value):
        return value or None


class Issue(Record):
    id: str
    integration_id: str
    evidence_id: str
    summary: str
    details: TicketDetails = Field(default_factory=TicketDetails)


class Dataset(Record):
    synthetic: Literal[True]
    as_of: datetime
    accounts: list[Account]
    integrations: list[Integration]
    evidence: list[Evidence]
    issues: list[Issue]

    @model_validator(mode="after")
    def references_are_consistent(self):
        groups = [self.accounts, self.integrations, self.evidence, self.issues]
        for records in groups:
            ids = [r.id for r in records]
            if len(ids) != len(set(ids)):
                raise ValueError("Duplicate record identifier")
        account_ids = {a.id for a in self.accounts}
        integrations = {i.id: i for i in self.integrations}
        evidence = {e.id: e for e in self.evidence}
        dates = [self.as_of] + [a.target_launch for a in self.accounts]
        dates += [e.at for e in self.evidence]
        if any(d.tzinfo is None for d in dates):
            raise ValueError("All timestamps must include a timezone")
        if any(e.at > self.as_of for e in self.evidence):
            raise ValueError("Evidence cannot be from the future")
        for e in self.evidence:
            if e.account_id not in account_ids:
                raise ValueError("Unknown evidence account scope")
            if e.integration_id is not None:
                if e.integration_id not in integrations:
                    raise ValueError("Unknown evidence integration scope")
                if integrations[e.integration_id].account_id != e.account_id:
                    raise ValueError("Evidence integration scope does not belong to its account")
            if e.claims and (
                e.integration_id is None or e.kind not in ("test_record", "customer_report")
            ):
                raise ValueError("Check claims require a scoped customer report or test record")
            if e.kind == "contact_record" and e.integration_id is not None:
                raise ValueError("Contact records have account scope only")
        for a in self.accounts:
            for eid in a.contact_ids:
                if eid not in evidence or evidence[eid].kind != "contact_record":
                    raise ValueError("Contacts must reference actual contact records")
                if evidence[eid].account_id != a.id:
                    raise ValueError("Contact evidence account scope does not match account")
        for i in self.integrations:
            if i.account_id not in account_ids:
                raise ValueError("Unknown account reference")
            for check_id, fact in i.facts.items():
                if fact.status in ("met", "not_met") and not fact.evidence_ids:
                    raise ValueError("Known facts require supporting evidence")
                if any(eid not in evidence for eid in fact.evidence_ids):
                    raise ValueError("Unknown evidence reference")
                if len(fact.evidence_ids) != len(set(fact.evidence_ids)):
                    raise ValueError("Duplicate fact evidence reference")
                for eid in fact.evidence_ids:
                    source = evidence[eid]
                    if source.integration_id != i.id:
                        raise ValueError(
                            "Fact evidence integration scope does not match integration"
                        )
                    if check_id not in source.claims:
                        raise ValueError("Fact evidence check scope does not match check")
                    if fact.status in ("met", "not_met") and source.claims[check_id] != fact.status:
                        raise ValueError(
                            "Evidence claim conflicts with fact state; preserve uncertainty"
                        )
        for issue in self.issues:
            if issue.integration_id not in integrations or issue.evidence_id not in evidence:
                raise ValueError("Broken issue reference")
            source = evidence[issue.evidence_id]
            if source.integration_id != issue.integration_id:
                raise ValueError("Issue evidence integration scope does not match integration")
            if source.kind not in ("customer_report", "test_record"):
                raise ValueError("Issue evidence must be a customer report or test record")
        return self
