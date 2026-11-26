import pytest

import app.services.subscriptions.cancel_user_subscription as module
from app.exceptions.payment_provider_error import PaymentProviderError
from app.exceptions.subscription_action_error import SubscriptionActionError
from app.types.authenticated_user import AuthenticatedUser
from tests.conftest import make_subscription


def make_user(plan="nextmove"):
    return AuthenticatedUser("user-1", "Jane Doe", "jane@example.com", True, {}, [], plan)


class FakeProvider:
    def __init__(self, error=None):
        self.error = error
        self.cancelled = []

    def cancel_subscription(self, subscription_id):
        if self.error:
            raise self.error
        self.cancelled.append(subscription_id)


def install(monkeypatch, record, provider):
    ended = []
    monkeypatch.setattr(module, "find_subscription_row", lambda column, value: record)
    monkeypatch.setattr(module, "get_payment_provider", lambda: provider)
    monkeypatch.setattr(
        module, "end_subscription", lambda record, now: ended.append(record) or "ended"
    )
    return ended


def test_cancels_with_the_provider_ends_the_plan_and_returns_explore(monkeypatch):
    provider = FakeProvider()
    ended = install(monkeypatch, make_subscription(), provider)

    status = module.cancel_user_subscription(make_user())

    assert provider.cancelled == ["mem_1"]
    assert ended[0].user_id == "user-1"
    assert (status.plan, status.is_paid, status.can_cancel) == ("explore", False, False)


def test_a_user_without_a_paid_subscription_is_refused(monkeypatch):
    provider = FakeProvider()
    install(monkeypatch, None, provider)

    with pytest.raises(SubscriptionActionError) as error:
        module.cancel_user_subscription(make_user("explore"))

    assert error.value.status_code == 400 and provider.cancelled == []


def test_a_subscription_that_is_already_cancelled_is_left_alone(monkeypatch):
    provider = FakeProvider()
    ended = install(monkeypatch, make_subscription(cancel_at_period_end=True), provider)

    status = module.cancel_user_subscription(make_user())

    assert status.cancel_at_period_end is True
    assert provider.cancelled == [] and ended == []


def test_a_provider_failure_is_raised_and_the_row_is_not_marked(monkeypatch):
    ended = install(monkeypatch, make_subscription(), FakeProvider(PaymentProviderError("down")))

    with pytest.raises(PaymentProviderError):
        module.cancel_user_subscription(make_user())
    assert ended == []


def test_an_explore_user_with_a_leftover_membership_id_is_refused(monkeypatch):
    provider = FakeProvider()
    install(monkeypatch, make_subscription(), provider)

    with pytest.raises(SubscriptionActionError):
        module.cancel_user_subscription(make_user("explore"))
    assert provider.cancelled == []
