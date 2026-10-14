import pytest

from csm_copilot.engine import Copilot


@pytest.mark.parametrize("as_of", [None, "2026-10-14T05:00:00-04:00"])
def test_same_instant_reports_the_dataset_snapshot(as_of):
    result = Copilot().list_accounts(as_of=as_of)
    assert result["dataset_as_of"] == "2026-10-14T09:00:00+00:00"
    assert result["time_basis"] == "dataset_snapshot"
    assert result["records_refreshed"] is False


def test_later_date_recalculates_age_without_refreshing_customer_records():
    engine = Copilot()
    before = engine.data.model_dump(mode="json")
    result = engine.list_accounts(as_of="2026-10-17T09:00:00Z")
    accounts = {a["account_id"]: a for a in result["accounts"]}
    assert result["as_of"] == "2026-10-17T09:00:00+00:00"
    assert result["dataset_as_of"] == "2026-10-14T09:00:00+00:00"
    assert result["time_basis"] == "recalculated_from_snapshot"
    assert result["records_refreshed"] is False
    assert "does not refresh" in result["time_boundary"]
    assert accounts["acc_014"]["days_since_contact"] == 8
    assert accounts["acc_014"]["stage"] == "validation"
    assert accounts["acc_014"]["last_contact"] == "2026-10-09T09:00:00+00:00"
    assert engine.check_readiness("lantern_android")["as_of"] == result["dataset_as_of"]
    assert engine.data.model_dump(mode="json") == before


@pytest.mark.parametrize("as_of", ["", " "])
def test_explicit_empty_date_is_not_an_implicit_default(as_of):
    with pytest.raises(ValueError):
        Copilot().list_accounts(as_of=as_of)
