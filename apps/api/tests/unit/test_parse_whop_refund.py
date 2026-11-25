from app.services.payments.whop.parse_whop_refund import parse_whop_refund

DATA = {
    "id": "rf_1",
    "amount": 6.9,
    "status": "succeeded",
    "payment": {"id": "pay_1", "membership": {"id": "mem_1"}},
}


def test_reads_the_refund_the_payment_the_membership_and_the_cents():
    notice = parse_whop_refund(DATA)

    assert (notice.refund_id, notice.payment_id, notice.membership_id) == ("rf_1", "pay_1", "mem_1")
    assert (notice.amount_cents, notice.status) == (690, "succeeded")


def test_a_refund_of_a_payment_without_a_membership_has_none():
    notice = parse_whop_refund({**DATA, "payment": {"id": "pay_1", "membership": None}})

    assert notice.membership_id is None


def test_an_unreadable_amount_gives_none():
    assert parse_whop_refund({**DATA, "amount": None}).amount_cents is None


def test_a_refund_without_a_payment_is_refused():
    assert parse_whop_refund({"id": "rf_1", "amount": 5, "status": "succeeded"}) is None
