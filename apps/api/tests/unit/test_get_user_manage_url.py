import pytest

import app.services.subscriptions.get_user_manage_url as module
from app.exceptions.payment_provider_error import PaymentProviderError
from app.exceptions.subscription_action_error import SubscriptionActionError
from app.types.authenticated_user import AuthenticatedUser
from tests.conftest import make_subscription


def make_user(plan="nextmove"):
    return AuthenticatedUser("user-1", "Jane Doe", "jane@example.com", True, {}, [], plan)


class FakeProvider:
    def __init__(self, url="https://whop.com/billing/manage/mem_1", error=None):
        self.url = url
        self.error = error
        self.asked = []

    def get_manage_url(self, subscription_id):
        if self.error:
            raise self.error
        self.asked.append(subscription_id)
        return self.url


def install(monkeypatch, record, provider):
    monkeypatch.setattr(module, "find_subscription_row", lambda column, value: record)
    monkeypatch.setattr(module, "get_payment_provider", lambda: provider)


def test_returns_the_providers_billing_page_for_the_users_membership(monkeypatch):
    provider = FakeProvider()
    install(monkeypatch, make_subscription(), provider)

    assert module.get_user_manage_url(make_user()) == "https://whop.com/billing/manage/mem_1"
    assert provider.asked == ["mem_1"]


def test_a_user_without_a_paid_subscription_gets_a_404(monkeypatch):
    install(monkeypatch, None, FakeProvider())

    with pytest.raises(SubscriptionActionError) as error:
        module.get_user_manage_url(make_user("explore"))

    assert error.value.status_code == 404


def test_a_provider_without_a_billing_page_gets_a_404(monkeypatch):
    install(monkeypatch, make_subscription(), FakeProvider(url=None))

    with pytest.raises(SubscriptionActionError) as error:
        module.get_user_manage_url(make_user())

    assert error.value.status_code == 404


def test_a_provider_failure_is_raised(monkeypatch):
    install(monkeypatch, make_subscription(), FakeProvider(error=PaymentProviderError("down")))

    with pytest.raises(PaymentProviderError):
        module.get_user_manage_url(make_user())
