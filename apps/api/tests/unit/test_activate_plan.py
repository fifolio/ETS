from datetime import UTC, datetime

import app.services.payments.activate_plan as module
from tests.conftest import make_notice, make_subscription

NOW = datetime(2026, 12, 5, tzinfo=UTC)


def install(monkeypatch, current=None):
    calls = []
    monkeypatch.setattr(module, "find_subscription_row", lambda column, value: current)
    monkeypatch.setattr(
        module, "set_user_plan", lambda user_id, plan: calls.append(("label", user_id, plan))
    )
    monkeypatch.setattr(
        module,
        "update_subscription_row",
        lambda user_id, data: calls.append(("row", user_id, data)),
    )
    monkeypatch.setattr(module, "apply_plan_credits", lambda *args: calls.append(("credits", args)))
    monkeypatch.setattr(
        module, "cancel_replaced_membership", lambda mid: calls.append(("cancel", mid))
    )
    return calls


def test_sets_the_plan_label_the_subscription_row_and_the_monthly_credits(monkeypatch):
    calls = install(monkeypatch)
    notice = make_notice(sku="plan_nextmove", membership_id="mem_1", customer_id="mber_1")

    module.activate_plan(notice, "nextmove", NOW)

    row = calls[0][2]
    assert (row["plan"], row["status"], row["providerSubscriptionId"]) == (
        "nextmove",
        "active",
        "mem_1",
    )
    assert calls[1] == ("label", "user-1", "nextmove")
    assert (row["providerCustomerId"], row["cancelAtPeriodEnd"], "startedAt" in row) == (
        "mber_1",
        False,
        False,
    )
    assert calls[2] == ("credits", ("user-1", "nextmove", "pay_1"))


def test_the_provisional_period_is_30_days_from_the_payment(monkeypatch):
    calls = install(monkeypatch)

    module.activate_plan(make_notice(sku="plan_urgent"), "urgent", NOW)

    assert calls[0][2]["currentPeriodEnd"] == "2026-12-31T10:00:00+00:00"


def test_without_a_payment_date_the_period_starts_now(monkeypatch):
    calls = install(monkeypatch)

    module.activate_plan(make_notice(paid_at=None), "nextmove", NOW)

    assert calls[0][2]["currentPeriodEnd"] == "2027-01-04T00:00:00+00:00"


def test_an_upgrade_cancels_the_membership_it_replaces(monkeypatch):
    calls = install(monkeypatch, make_subscription(membership_id="mem_old"))

    module.activate_plan(make_notice(sku="plan_urgent", membership_id="mem_new"), "urgent", NOW)

    assert ("cancel", "mem_old") in calls
    assert [call[0] for call in calls] == ["row", "label", "credits", "cancel"]


def test_an_old_membership_cancellation_arrives_after_the_new_membership_is_current(monkeypatch):
    current = make_subscription(membership_id="mem_old")
    events = []

    def find_row(column, value):
        if column == "$id" or current.membership_id == value:
            return current
        return None

    monkeypatch.setattr(module, "find_subscription_row", find_row)
    monkeypatch.setattr(module, "set_user_plan", lambda user_id, plan: None)

    def update_row(user_id, data):
        nonlocal current
        current = make_subscription(
            user_id=user_id,
            plan=data["plan"],
            membership_id=data["providerSubscriptionId"],
        )

    monkeypatch.setattr(module, "update_subscription_row", update_row)
    monkeypatch.setattr(module, "apply_plan_credits", lambda *args: None)

    def cancel_replaced(membership_id):
        events.append(membership_id)
        events.append(
            module.find_subscription_row("providerSubscriptionId", membership_id)
        )

    monkeypatch.setattr(module, "cancel_replaced_membership", cancel_replaced)

    module.activate_plan(make_notice(sku="plan_urgent", membership_id="mem_new"), "urgent", NOW)

    assert events == ["mem_old", None]


def test_a_renewal_of_the_same_membership_cancels_nothing(monkeypatch):
    calls = install(monkeypatch, make_subscription(membership_id="mem_1"))

    module.activate_plan(make_notice(sku="plan_nextmove", membership_id="mem_1"), "nextmove", NOW)

    assert not any(call[0] == "cancel" for call in calls)


def test_a_first_purchase_with_nothing_to_replace_cancels_nothing(monkeypatch):
    calls = install(monkeypatch, make_subscription(plan="explore", membership_id=None))

    module.activate_plan(make_notice(sku="plan_nextmove", membership_id="mem_1"), "nextmove", NOW)

    assert not any(call[0] == "cancel" for call in calls)
