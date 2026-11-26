from fastapi.testclient import TestClient

from app.main import app
from app.schemas.payment_entry_out import PaymentEntryOut

client = TestClient(app)


def test_returns_the_payment_history_of_the_logged_in_user(monkeypatch, logged_in):
    asked = []
    entry = PaymentEntryOut(
        sku="topup", amount_cents=500, credits=40, status="completed", paid_at=None
    )
    monkeypatch.setattr(
        "app.routers.payments.list_payment_history",
        lambda user_id: asked.append(user_id) or [entry],
    )

    response = client.get("/payments")

    assert response.status_code == 200 and response.json() == [entry.model_dump()]
    assert asked == ["user-1"]
