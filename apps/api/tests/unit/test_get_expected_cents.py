from app.services.payments.get_expected_cents import get_expected_cents
from tests.conftest import make_notice, make_record


def test_our_record_of_the_checkout_wins():
    assert get_expected_cents(make_notice(paid_cents=999), make_record(amount_cents=500)) == 500


def test_a_record_without_an_amount_falls_back_to_the_catalog():
    notice = make_notice(sku="plan_nextmove", paid_cents=700)

    assert get_expected_cents(notice, make_record(sku="plan_nextmove", amount_cents=0)) == 700


def test_a_plan_without_a_record_costs_its_catalog_price():
    assert get_expected_cents(make_notice(sku="plan_urgent", paid_cents=1400), None) == 1400


def test_a_top_up_without_a_record_is_what_was_paid_if_it_is_a_valid_amount():
    assert get_expected_cents(make_notice(sku="topup", paid_cents=525), None) == 525


def test_a_top_up_without_a_record_that_is_not_a_valid_amount_has_no_expected_price():
    assert get_expected_cents(make_notice(sku="topup", paid_cents=40), None) is None


def test_an_unknown_product_has_no_expected_price():
    assert get_expected_cents(make_notice(sku="plan_platinum"), None) is None
