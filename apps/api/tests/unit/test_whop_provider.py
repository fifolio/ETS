import pytest

import app.services.payments.whop.whop_provider as module
from app.core.config import settings
from app.exceptions.configuration_error import ConfigurationError
from app.types.checkout_order import CheckoutOrder
from app.types.whop_settings import WhopSettings

PLAN_ORDER = CheckoutOrder("user-1", "jane@example.com", "plan_nextmove", 700, 150)
TOPUP_ORDER = CheckoutOrder("user-1", "jane@example.com", "topup", 525, 42)
REDIRECT = "http://localhost:3000/settings?payment=success"


def install(monkeypatch, plan_ids=None, topup_product="prod_topup"):
    sent = []
    whop = WhopSettings(
        "sandbox", "https://api", "https://sandbox.whop.com", "key", plan_ids or {}, topup_product
    )

    def fake_post(whop_settings, body):
        sent.append(body)
        return {
            "id": "ch_1",
            "purchase_url": "https://sandbox.whop.com/checkout/plan_9/?session=ch_1",
            "variant": {"id": "plan_9"},
        }

    monkeypatch.setattr(module, "get_whop_settings", lambda: whop)
    monkeypatch.setattr(module, "post_checkout_configuration", fake_post)
    monkeypatch.setattr(settings, "payment_success_url", REDIRECT)
    return sent


def test_a_plan_checkout_uses_the_existing_plan_and_puts_the_buyer_in_the_metadata(monkeypatch):
    sent = install(monkeypatch, {"plan_nextmove": "plan_1"})

    session = module.WhopProvider().create_checkout(PLAN_ORDER)

    assert sent == [
        {
            "variant_id": "plan_1",
            "metadata": {"ets_user_id": "user-1", "ets_sku": "plan_nextmove"},
            "redirect_url": REDIRECT,
        }
    ]
    assert (session.checkout_id, session.plan_id) == ("ch_1", "plan_9")


def test_a_top_up_checkout_creates_a_one_time_variant_priced_in_dollars(monkeypatch):
    sent = install(monkeypatch)

    session = module.WhopProvider().create_checkout(TOPUP_ORDER)

    body = sent[0]
    assert "variant_id" not in body
    assert body["variant"] == {
        "billing_type": "one_time",
        "currency": "usd",
        "initial_price": 5.25,
        "title": "ETS credits (42)",
        "description": "42 ETS credits",
        "product_id": "prod_topup",
    }
    assert body["metadata"] == {"ets_user_id": "user-1", "ets_sku": "topup"}
    assert session.plan_id == "plan_9"


def test_a_top_up_without_a_configured_product_leaves_the_product_out(monkeypatch):
    sent = install(monkeypatch, topup_product="")

    module.WhopProvider().create_checkout(TOPUP_ORDER)

    assert "product_id" not in sent[0]["variant"]


def test_a_plan_without_a_plan_id_is_a_configuration_error(monkeypatch):
    install(monkeypatch, {"plan_nextmove": ""})

    with pytest.raises(ConfigurationError):
        module.WhopProvider().create_checkout(PLAN_ORDER)


def test_reports_its_name_and_the_configured_environment(monkeypatch):
    monkeypatch.setattr(settings, "whop_environment", "production")

    provider = module.WhopProvider()

    assert (provider.name, provider.environment) == ("whop", "production")
