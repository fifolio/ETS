import app.services.payments.whop.resolve_renewal_notice as module
from tests.conftest import make_subscription

DATA = {
    "id": "pay_9",
    "status": "paid",
    "currency": "usd",
    "total": {"amount": "7.00"},
    "membership_id": "mem_1",
    "metadata": {},
}


def test_a_renewal_without_metadata_is_matched_through_its_membership(monkeypatch):
    monkeypatch.setattr(
        module, "find_subscription_row", lambda column, value: make_subscription(plan="nextmove")
    )

    notice = module.resolve_renewal_notice(DATA, "sandbox")

    assert (notice.user_id, notice.sku, notice.paid_cents, notice.membership_id) == (
        "user-1",
        "plan_nextmove",
        700,
        "mem_1",
    )


def test_a_membership_we_dont_know_gives_none(monkeypatch):
    monkeypatch.setattr(module, "find_subscription_row", lambda column, value: None)

    assert module.resolve_renewal_notice(DATA, "sandbox") is None


def test_a_payment_without_a_membership_gives_none(monkeypatch):
    monkeypatch.setattr(module, "find_subscription_row", lambda column, value: make_subscription())

    assert module.resolve_renewal_notice({**DATA, "membership_id": None}, "sandbox") is None
