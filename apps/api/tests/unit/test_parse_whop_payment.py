from datetime import UTC, datetime

from app.services.payments.whop.parse_whop_payment import parse_whop_payment

DATA = {
    "id": "pay_1",
    "status": "paid",
    "currency": "USD",
    "total": {"amount": "5.25"},
    "metadata": {"ets_user_id": "user-1", "ets_sku": "topup"},
    "checkout_configuration_id": "ch_1",
    "membership_id": None,
    "member_id": "mber_1",
    "paid_at": "2026-12-01T10:00:00.000Z",
}


def test_reads_the_neutral_fields():
    notice = parse_whop_payment(DATA, "sandbox")

    assert (notice.provider, notice.environment, notice.payment_id) == ("whop", "sandbox", "pay_1")
    assert (notice.user_id, notice.sku, notice.checkout_id) == ("user-1", "topup", "ch_1")
    assert (notice.paid_cents, notice.membership_id, notice.customer_id) == (525, None, "mber_1")
    assert notice.paid_at == datetime(2026, 12, 1, 10, 0, tzinfo=UTC)


def test_the_currency_is_lower_cased():
    assert parse_whop_payment(DATA, "sandbox").currency == "usd"


def test_a_payment_without_our_metadata_is_not_ours():
    assert parse_whop_payment({**DATA, "metadata": {"order_ref": "x"}}, "sandbox") is None


def test_a_payment_without_an_id_is_refused():
    assert parse_whop_payment({**DATA, "id": None}, "sandbox") is None


def test_an_unreadable_total_gives_no_amount():
    assert parse_whop_payment({**DATA, "total": None}, "sandbox").paid_cents is None
