import pytest

from app.core.config import settings
from app.exceptions.configuration_error import ConfigurationError
from app.services.payments.whop.get_whop_settings import get_whop_settings


def fill(monkeypatch, environment, key):
    monkeypatch.setattr(settings, f"whop_{environment}_api_key", key)
    monkeypatch.setattr(
        settings, f"whop_{environment}_plan_nextmove", f"{environment}-plan_nextmove"
    )
    monkeypatch.setattr(settings, f"whop_{environment}_plan_urgent", f"{environment}-plan_urgent")
    monkeypatch.setattr(
        settings, f"whop_{environment}_product_topup", f"{environment}-product_topup"
    )
    monkeypatch.setattr(settings, f"whop_{environment}_webhook_secret", f"{environment}-secret")


def test_sandbox_uses_the_sandbox_key_addresses_and_plans(monkeypatch):
    monkeypatch.setattr(settings, "whop_environment", "sandbox")
    fill(monkeypatch, "sandbox", "sandbox-key")
    fill(monkeypatch, "production", "production-key")

    result = get_whop_settings()

    assert result.api_base == "https://sandbox-api.whop.com/api/v1"
    assert result.checkout_host == "https://sandbox.whop.com"
    assert (result.environment, result.api_key) == ("sandbox", "sandbox-key")
    assert result.plan_ids["plan_nextmove"] == "sandbox-plan_nextmove"
    assert result.webhook_secret == "sandbox-secret"


def test_production_uses_only_the_production_values(monkeypatch):
    monkeypatch.setattr(settings, "whop_environment", "production")
    fill(monkeypatch, "sandbox", "sandbox-key")
    fill(monkeypatch, "production", "production-key")

    result = get_whop_settings()

    assert result.api_base == "https://api.whop.com/api/v1"
    assert (result.environment, result.api_key) == ("production", "production-key")
    assert result.topup_product_id == "production-product_topup"


def test_a_missing_key_is_a_configuration_error(monkeypatch):
    monkeypatch.setattr(settings, "whop_environment", "sandbox")
    fill(monkeypatch, "sandbox", "")

    with pytest.raises(ConfigurationError):
        get_whop_settings()


def test_an_unknown_environment_is_a_configuration_error(monkeypatch):
    monkeypatch.setattr(settings, "whop_environment", "staging")

    with pytest.raises(ConfigurationError):
        get_whop_settings()


def test_the_two_plans_and_the_top_up_product_are_all_there(monkeypatch):
    monkeypatch.setattr(settings, "whop_environment", "sandbox")
    fill(monkeypatch, "sandbox", "key")

    result = get_whop_settings()

    assert set(result.plan_ids) == {"plan_nextmove", "plan_urgent"}
    assert result.topup_product_id == "sandbox-product_topup"
