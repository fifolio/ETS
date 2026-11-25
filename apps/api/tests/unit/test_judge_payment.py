import pytest

from app.services.payments.judge_payment import judge_payment
from tests.conftest import make_notice, make_record


def verdict(notice, template=None):
    result = judge_payment(notice, template)
    return result.outcome, result.status, result.expected_cents


def test_a_plan_paid_at_the_catalog_price_is_ok():
    assert verdict(make_notice(sku="plan_nextmove", paid_cents=700)) == ("ok", "completed", 700)


def test_a_top_up_paid_as_recorded_is_ok():
    assert verdict(make_notice(paid_cents=500), make_record(amount_cents=500)) == (
        "ok",
        "completed",
        500,
    )


def test_paying_more_than_expected_is_still_ok():
    assert verdict(make_notice(paid_cents=600), make_record(amount_cents=500)) == (
        "ok",
        "completed",
        500,
    )


def test_paying_less_than_expected_is_underpaid():
    assert verdict(make_notice(paid_cents=400), make_record(amount_cents=500)) == (
        "underpaid",
        "underpaid",
        500,
    )


def test_another_currency_is_refused():
    assert verdict(make_notice(currency="eur"))[0] == "unsupported_currency"


def test_an_unreadable_amount_is_refused():
    assert verdict(make_notice(paid_cents=None))[0] == "unverifiable"


@pytest.mark.parametrize(("user_id", "sku"), [("other-user", "topup"), ("user-1", "plan_urgent")])
def test_a_payment_that_disagrees_with_our_record_is_refused(user_id, sku):
    assert verdict(make_notice(), make_record(user_id=user_id, sku=sku))[0] == "mismatch"


def test_a_top_up_with_no_record_and_an_invalid_amount_is_refused():
    assert verdict(make_notice(sku="topup", paid_cents=40))[0] == "invalid_amount"
