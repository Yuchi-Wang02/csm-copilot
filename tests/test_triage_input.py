"""Known record identifiers must not masquerade as customer prose."""

import pytest

from csm_copilot.engine import Copilot


@pytest.mark.parametrize("value", ["issue_callback", " issue_callback ", "issue_blank"])
def test_known_issue_identifier_requires_message_or_recorded_issue_tool(value):
    engine = Copilot()
    before = engine.data.model_dump(mode="json")
    with pytest.raises(ValueError, match="customer message, not a recorded issue ID"):
        engine.triage_issue(value)
    assert engine.data.model_dump(mode="json") == before


@pytest.mark.parametrize(
    "value", ["Callback failed.", "回调失败。", "For issue_callback, the reward has not arrived."]
)
def test_customer_prose_remains_accepted_including_an_identifier_in_context(value):
    result = Copilot().triage_issue(value, "harbor_android")
    assert [c["category"] for c in result["candidates"]] == ["reward_callback"]
