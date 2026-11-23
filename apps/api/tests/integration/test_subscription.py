import pytest
from fastapi.testclient import TestClient

from app.dependencies.get_current_user import get_current_user
from app.main import app
from app.types.authenticated_user import AuthenticatedUser
from app.types.checkout_session import CheckoutSession

client = TestClient(app)
URL = "/subscription/checkout"


class FakeProvider:
    name = "fake"
    environment = "sandbox"

    def __init__(self, error=None):
        self.error = error
        self.orders = []

    def create_checkout(self, order):
        if self.error:
            raise self.error
        self.orders.append(order)
        return CheckoutSession("ch_1", "plan_1", "https://pay.example/1")


def install(monkeypatch, provider):
    recorded = []
    monkeypatch.setattr("app.routers.subscription.get_payment_provider", lambda: provider)
    monkeypatch.setattr(
        "app.routers.subscription.record_pending_payment", lambda *args: recorded.append(args)
    )
    return recorded


def as_user(plan):
    user = AuthenticatedUser("user-1", "Jane Doe", "jane.doe@example.com", True, {}, [], plan)
    app.dependency_overrides[get_current_user] = lambda: user


def test_checkout_returns_the_session_the_price_and_the_credits(monkeypatch, logged_in):
    provider = FakeProvider()
    recorded = install(monkeypatch, provider)

    response = client.post(URL, json={"product": "nextmove"})

    assert response.status_code == 200
    assert response.json() == {
        "provider": "fake",
        "environment": "sandbox",
        "checkout_id": "ch_1",
        "plan_id": "plan_1",
        "checkout_url": "https://pay.example/1",
        "amount_cents": 700,
        "credits": 150,
    }
    assert recorded[0][2:] == ("fake", "sandbox")


def test_a_top_up_is_priced_from_the_amount_on_the_server(monkeypatch, logged_in):
    provider = FakeProvider()
    install(monkeypatch, provider)

    body = client.post(URL, json={"product": "topup", "amount_usd": 5}).json()

    assert (body["amount_cents"], body["credits"]) == (500, 40)
    order = provider.orders[0]
    assert (order.sku, order.amount_cents, order.credits) == ("topup", 500, 40)


def test_a_top_up_costs_the_same_for_an_urgent_user(monkeypatch, logged_in):
    provider = FakeProvider()
    install(monkeypatch, provider)
    as_user("urgent")

    client.post(URL, json={"product": "topup", "amount_usd": 5})

    assert (provider.orders[0].amount_cents, provider.orders[0].credits) == (500, 40)


@pytest.mark.parametrize(
    "payload",
    [
        {"product": "topup", "amount_usd": 0.75},
        {"product": "topup", "amount_usd": 50.25},
        {"product": "topup", "amount_usd": 5.10},
        {"product": "topup"},
    ],
)
def test_a_top_up_outside_the_rules_is_refused(monkeypatch, logged_in, payload):
    install(monkeypatch, FakeProvider())

    assert client.post(URL, json=payload).status_code == 400
