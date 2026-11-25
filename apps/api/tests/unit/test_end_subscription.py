from datetime import UTC, datetime

import app.services.payments.end_subscription as module
from tests.conftest import make_subscription

NOW = datetime(2026, 12, 31, tzinfo=UTC)


def install(monkeypatch):
    calls = []
    monkeypatch.setattr(module, "apply_plan_credits", lambda *args: calls.append(("credits", args)))
    monkeypatch.setattr(
        module, "set_user_plan", lambda user_id, plan: calls.append(("label", user_id, plan))
    )
    monkeypatch.setattr(
        module, "update_subscription_row", lambda user_id, data: calls.append(("row", data))
    )
    monkeypatch.setattr(module, "send_notification", lambda *args: calls.append(("notify", args)))
    return calls


def test_a_paid_plan_goes_back_to_explore_with_explores_monthly_credits(monkeypatch):
    calls = install(monkeypatch)

    assert module.end_subscription(make_subscription(), NOW) == "ended"

    assert calls[0] == ("credits", ("user-1", "explore", "end:mem_1"))
    assert calls[1] == ("label", "user-1", "explore")
    row = calls[2][1]
    assert (row["plan"], row["providerSubscriptionId"], row["currentPeriodEnd"]) == (
        "explore",
        None,
        None,
    )
    assert calls[3][0] == "notify"


def test_the_row_is_updated_last_so_a_failed_attempt_can_be_repeated(monkeypatch):
    calls = install(monkeypatch)

    module.end_subscription(make_subscription(), NOW)

    assert [call[0] for call in calls] == ["credits", "label", "row", "notify"]


def test_an_explore_account_has_nothing_to_end(monkeypatch):
    calls = install(monkeypatch)

    assert (
        module.end_subscription(make_subscription(plan="explore", membership_id=None), NOW)
        == "ignored"
    )
    assert calls == []
