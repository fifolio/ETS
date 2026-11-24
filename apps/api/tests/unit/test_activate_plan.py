from datetime import UTC, datetime

import app.services.payments.activate_plan as module
from tests.conftest import make_notice

NOW = datetime(2026, 12, 5, tzinfo=UTC)


def install(monkeypatch):
    calls = []
    monkeypatch.setattr(
        module, "set_user_plan", lambda user_id, plan: calls.append(("label", user_id, plan))
    )
    monkeypatch.setattr(
        module,
        "update_subscription_row",
        lambda user_id, data: calls.append(("row", user_id, data)),
    )
    monkeypatch.setattr(module, "apply_plan_credits", lambda *args: calls.append(("credits", args)))
    return calls


def test_sets_the_plan_label_the_subscription_row_and_the_monthly_credits(monkeypatch):
    calls = install(monkeypatch)
    notice = make_notice(sku="plan_nextmove", membership_id="mem_1", customer_id="mber_1")

    module.activate_plan(notice, "nextmove", NOW)

    assert calls[0] == ("label", "user-1", "nextmove")
    row = calls[1][2]
    assert (row["plan"], row["status"], row["providerSubscriptionId"]) == (
        "nextmove",
        "active",
        "mem_1",
    )
    assert (row["providerCustomerId"], row["cancelAtPeriodEnd"]) == ("mber_1", False)
    assert calls[2] == ("credits", ("user-1", "nextmove", "pay_1"))


def test_the_provisional_period_is_30_days_from_the_payment(monkeypatch):
    calls = install(monkeypatch)

    module.activate_plan(make_notice(sku="plan_urgent"), "urgent", NOW)

    assert calls[1][2]["currentPeriodEnd"] == "2025-12-31T10:00:00+00:00".replace("2025", "2026")


def test_without_a_payment_date_the_period_starts_now(monkeypatch):
    calls = install(monkeypatch)

    module.activate_plan(make_notice(paid_at=None), "nextmove", NOW)

    assert calls[1][2]["startedAt"] == NOW.isoformat()
