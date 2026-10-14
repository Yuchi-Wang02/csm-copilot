"""Validate fixture boundaries before any tool uses customer evidence."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Status = Literal["met", "not_met", "unknown", "not_applicable"]


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Evidence(Record):
    id: str
    at: datetime
    kind: Literal["customer_report", "test_record", "sales_handoff", "contact_record"]
    text: str


class Fact(Record):
    status: Status
    evidence_ids: list[str] = Field(default_factory=list)


class Integration(Record):
    id: str
    account_id: str
    app: str
    platform: Literal["Android", "iOS"]
    currency_mode: Literal["self_managed", "tapjoy_managed"]
    facts: dict[str, Fact]


class Account(Record):
    id: str
    name: str
    stage: Literal["integration", "validation", "live"]
    target_launch: datetime
    contact_ids: list[str]


class Issue(Record):
    id: str
    integration_id: str
    evidence_id: str
    summary: str
    details: dict[str, str] = Field(default_factory=dict)


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
        integration_ids = {i.id for i in self.integrations}
        evidence = {e.id: e for e in self.evidence}
        dates = [self.as_of] + [a.target_launch for a in self.accounts]
        dates += [e.at for e in self.evidence]
        if any(d.tzinfo is None for d in dates):
            raise ValueError("All timestamps must include a timezone")
        if any(e.at > self.as_of for e in self.evidence):
            raise ValueError("Evidence cannot be from the future")
        for a in self.accounts:
            for eid in a.contact_ids:
                if eid not in evidence or evidence[eid].kind != "contact_record":
                    raise ValueError("Contacts must reference actual contact records")
        for i in self.integrations:
            if i.account_id not in account_ids:
                raise ValueError("Unknown account reference")
            for fact in i.facts.values():
                if fact.status in ("met", "not_met") and not fact.evidence_ids:
                    raise ValueError("Known facts require supporting evidence")
                if any(eid not in evidence for eid in fact.evidence_ids):
                    raise ValueError("Unknown evidence reference")
        for issue in self.issues:
            if issue.integration_id not in integration_ids or issue.evidence_id not in evidence:
                raise ValueError("Broken issue reference")
        return self
