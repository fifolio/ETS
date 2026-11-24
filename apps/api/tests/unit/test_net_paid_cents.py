from app.services.payments.whop.net_paid_cents import net_paid_cents


def money(amount):
    return {"amount": amount, "currency": "usd"}


def test_the_total_is_what_was_paid_when_there_is_no_tax():
    assert net_paid_cents({"total": money("5.00")}) == 500


def test_tax_added_on_top_is_taken_out():
    data = {"total": money("5.40"), "tax_amount": money("0.40"), "tax_behavior": "exclusive"}

    assert net_paid_cents(data) == 500


def test_tax_already_inside_the_price_is_not_taken_out():
    data = {"total": money("5.00"), "tax_amount": money("0.45"), "tax_behavior": "inclusive"}

    assert net_paid_cents(data) == 500


def test_tax_of_an_unknown_kind_is_not_taken_out():
    data = {"total": money("5.40"), "tax_amount": money("0.40"), "tax_behavior": None}

    assert net_paid_cents(data) == 540


def test_a_missing_total_gives_none():
    assert net_paid_cents({"total": None}) is None
