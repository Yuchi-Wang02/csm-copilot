"""Keep the public boundary demonstration tied to observed engine/parser behavior."""

import json
import runpy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def report():
    return runpy.run_path(str(ROOT / "evaluation/trust_boundary.py"))["build_report"]()


@pytest.mark.parametrize("case_id", ["customer_en", "customer_zh"])
def test_instruction_text_is_retained_without_changing_structured_workflow(report, case_id):
    row = next(c for c in report["cases"] if c["id"] == case_id)
    result = row["result"]
    assert result["returned_text"] == row["input"]
    assert result["declared_language"] == case_id.removeprefix("customer_")
    assert row["input"] in result["ticket_title"]
    assert result["readiness"] == "blocked"
    assert result["readiness_equals_baseline"]
    assert result["queue_equals_baseline"]
    assert result["followup_equals_baseline"]
    assert result["dataset_unchanged_after_calls"]
    assert result["ticket_sent"] is False
    assert result["root_cause"] == "unconfirmed"


def test_unavailable_actions_do_not_return_even_a_partial_batch(report):
    cases = {c["id"]: c for c in report["cases"]}
    assert len(json.loads(cases["send_batch"]["input"])) == 2
    for key in ("send_batch", "write_fact"):
        result = cases[key]["result"]
        assert result["parser_accepted"] is False
        assert "actions" not in result
        assert "allowlist" in result["error"]
    assert "send_email" not in report["declared_read_only_tools"]
    assert "update_readiness" not in report["declared_read_only_tools"]


def test_account_ownership_is_not_presented_as_read_authorization(report):
    row = next(c for c in report["cases"] if c["id"] == "other_account")
    assert row["result"] == {
        "parser_accepted": True,
        "returned_account_id": "acc_006",
        "synthetic": True,
    }


def test_unsupported_final_remains_an_explicit_parser_and_lint_limit(report):
    row = next(c for c in report["cases"] if c["id"] == "false_final")
    assert row["result"]["parsed_final"] == json.loads(row["input"])["final"]
    assert row["result"]["lint"]["flags"] == []
    assert row["result"]["lint"]["semantic_verification"] == "not_performed"
    assert row["result"]["lint"]["human_review_required"] is True
    assert row["result"]["model_inference"] is False


def test_published_report_reproduces_without_mutating_fixture(report):
    assert report["baseline_fixture_unchanged"] is True
    assert len(report["cases"]) == 6
    assert len(report["declared_read_only_tools"]) == 8
    assert report == json.loads((ROOT / "evidence/trust-boundary.json").read_text(encoding="utf-8"))
