import app.services.payments.record_pending_payment as module
from app.types.checkout_order import CheckoutOrder
from app.types.checkout_session import CheckoutSession

ORDER = CheckoutOrder("user-1", "jane@example.com", "topup", 500, 40)
SESSION = CheckoutSession("ch_1", "plan_9", "https://pay.example/1")


def test_records_the_checkout_as_pending(monkeypatch):
    rows = []
    monkeypatch.setattr(module, "create_payment_row", rows.append)

    module.record_pending_payment(ORDER, SESSION, "whop", "sandbox")

    assert rows == [
        {
            "userId": "user-1",
            "provider": "whop",
            "environment": "sandbox",
            "sku": "topup",
            "providerCheckoutId": "ch_1",
            "amountCents": 500,
            "credits": 40,
            "currency": "usd",
            "status": "pending",
        }
    ]


def test_a_failing_save_never_raises(monkeypatch):
    def fail(data):
        raise RuntimeError("table down")

    monkeypatch.setattr(module, "create_payment_row", fail)

    module.record_pending_payment(ORDER, SESSION, "whop", "sandbox")
