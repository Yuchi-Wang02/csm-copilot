import hashlib
import json
from datetime import datetime
from pathlib import Path

import pytest

from csm_copilot.engine import Copilot
from csm_copilot.models import Dataset

ROOT = Path(__file__).resolve().parents[1]
BEFORE = json.loads((ROOT / "evidence/queue-order-before.json").read_text(encoding="utf-8"))


def engine_with_dates(overrides):
    data = Copilot().data.model_dump(mode="json")
    for account in data["accounts"]:
        if account["id"] in overrides:
            account["target_launch"] = overrides[account["id"]]
    return Copilot(Dataset.model_validate(data))


@pytest.mark.parametrize("case", BEFORE["cases"], ids=lambda case: case["id"])
def test_close_launches_follow_exact_time_not_rounded_days(case):
    assert (
        hashlib.sha256((ROOT / "src/csm_copilot/data/accounts.json").read_bytes()).hexdigest()
        == BEFORE["fixture_sha256"]
    )
    engine = engine_with_dates(case["target_launch_overrides"])
    original = engine.data.model_dump(mode="json")
    result = engine.list_accounts()
    assert [a["account_id"] for a in result["accounts"]] == case["expected_order"]
    assert [a["account_id"] for a in case["before_result"]["accounts"]] != case["expected_order"]
    # Only order changes: rounded values, missingness and selection stay intact.
    assert {a["account_id"]: a for a in result["accounts"]} == {
        a["account_id"]: a for a in case["before_result"]["accounts"]
    }
    dates = [engine.accounts[a["account_id"]].target_launch for a in result["accounts"]]
    assert dates == sorted(dates)
    assert engine.data.model_dump(mode="json") == original


def test_actual_time_ties_use_account_id_and_live_accounts_remain_last():
    engine = engine_with_dates(
        {"acc_014": "2026-10-16T11:01:00+02:00", "acc_006": "2026-10-16T09:01:00Z"}
    )
    result = engine.list_accounts(include_live=True)
    assert [a["account_id"] for a in result["accounts"]] == [
        "acc_006",
        "acc_014",
        "acc_018",
        "acc_009",
    ]
    assert engine.accounts["acc_014"].target_launch == datetime.fromisoformat(
        "2026-10-16T09:01:00Z"
    )
    assert result["accounts"][-1]["days_to_launch"] is None
    assert result["accounts"][-1]["launch_overdue"] is False
