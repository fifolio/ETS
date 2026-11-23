import pytest

from app.exceptions.payment_provider_error import PaymentProviderError
from app.services.payments.whop.parse_checkout_configuration import parse_checkout_configuration
from app.types.whop_settings import WhopSettings

WHOP = WhopSettings("sandbox", "https://api", "https://sandbox.whop.com", "key", {}, "")


def test_reads_the_ids_and_the_payment_page_address_from_the_answer():
    data = {
        "id": "ch_1",
        "purchase_url": "https://sandbox.whop.com/checkout/ch_1/",
        "variant": {"id": "plan_9"},
    }

    assert parse_checkout_configuration(data, WHOP, "plan_1") == (
        "ch_1",
        "https://sandbox.whop.com/checkout/ch_1/",
        "plan_9",
    )


def test_builds_the_address_when_whop_doesnt_send_one():
    data = {"id": "ch_1", "variant": {"id": "plan_9"}}

    assert parse_checkout_configuration(data, WHOP, None) == (
        "ch_1",
        "https://sandbox.whop.com/checkout/plan_9/?session=ch_1",
        "plan_9",
    )


def test_falls_back_to_the_plan_that_was_sent_when_the_answer_has_no_variant():
    assert parse_checkout_configuration({"id": "ch_1"}, WHOP, "plan_1") == (
        "ch_1",
        "https://sandbox.whop.com/checkout/plan_1/?session=ch_1",
        "plan_1",
    )


@pytest.mark.parametrize("data", [{}, {"id": ""}, {"id": 5}])
def test_a_missing_checkout_id_is_a_provider_error(data):
    with pytest.raises(PaymentProviderError):
        parse_checkout_configuration(data, WHOP, "plan_1")
