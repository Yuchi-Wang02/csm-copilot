"""Caller edits to returned data or constructor input must not alter the engine snapshot."""

from copy import deepcopy

import pytest
from pydantic import ValidationError

from csm_copilot.engine import Copilot, load_json
from csm_copilot.models import Dataset


@pytest.mark.parametrize("tool", ["readiness", "friction"])
def test_editing_returned_evidence_ids_preserves_the_source_and_next_result(tool):
    engine = Copilot()
    before = engine.data.model_dump(mode="json")
    call = (
        (lambda: engine.check_readiness("lantern_ios"))
        if tool == "readiness"
        else engine.friction_digest
    )
    result = call()
    expected = deepcopy(result)
    if tool == "readiness":
        refs = result["checks"][0]["evidence_ids"]
    else:
        theme = next(t for t in result["themes"] if t["check_id"] == "device_verified")
        refs = next(m["evidence_ids"] for m in theme["members"] if m["evidence_ids"])
    assert refs  # Exercise a real known fact, not an already empty unknown.
    refs.clear()
    assert engine.data.model_dump(mode="json") == before
    assert call() == expected


def test_constructor_owns_a_snapshot_separate_from_the_callers_dataset():
    source = Dataset.model_validate(load_json("accounts.json"))
    engine = Copilot(source)
    expected = engine.check_readiness("lantern_ios")
    original_name = engine.get_account_context("acc_014")["account"]["name"]
    ios = next(i for i in source.integrations if i.id == "lantern_ios")
    ios.facts["currency_approved"].evidence_ids.clear()
    next(a for a in source.accounts if a.id == "acc_014").name = "Caller changed this"
    assert engine.check_readiness("lantern_ios") == expected
    assert engine.get_account_context("acc_014")["account"]["name"] == original_name


def test_previously_valid_but_mutated_dataset_is_revalidated_at_construction():
    source = Dataset.model_validate(load_json("accounts.json"))
    ios = next(i for i in source.integrations if i.id == "lantern_ios")
    ios.facts["currency_approved"].evidence_ids.clear()
    with pytest.raises(ValidationError, match="Known facts require supporting evidence"):
        Copilot(source)
