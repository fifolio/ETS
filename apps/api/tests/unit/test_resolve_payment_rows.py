import app.services.payments.resolve_payment_rows as module

from tests.conftest import make_notice, make_record


def install(monkeypatch, by_payment=None, by_checkout=None):
    def fake_find(column, value):
        return by_payment if column == "providerPaymentId" else by_checkout

    monkeypatch.setattr(module, "find_payment_row", fake_find)


def test_a_payment_that_already_has_a_row_updates_that_row(monkeypatch):
    own = make_record(payment_id="pay_1")
    install(monkeypatch, by_payment=own)

    rows = module.resolve_payment_rows(make_notice())

    assert (rows.existing, rows.row, rows.template) == (own, own, own)


def test_the_pending_checkout_row_is_claimed_by_the_first_payment(monkeypatch):
    pending = make_record()
    install(monkeypatch, by_checkout=pending)

    rows = module.resolve_payment_rows(make_notice())

    assert (rows.existing, rows.row, rows.template) == (None, pending, pending)


def test_a_second_payment_on_the_same_checkout_gets_its_own_row_with_the_amounts_as_template(
    monkeypatch,
):
    first = make_record(payment_id="pay_0", applied=True)
    install(monkeypatch, by_checkout=first)

    rows = module.resolve_payment_rows(make_notice(payment_id="pay_1"))

    assert (rows.existing, rows.row, rows.template) == (None, None, first)


def test_a_payment_nobody_recorded_has_no_rows(monkeypatch):
    install(monkeypatch)

    rows = module.resolve_payment_rows(make_notice(checkout_id=""))

    assert (rows.existing, rows.row, rows.template) == (None, None, None)
