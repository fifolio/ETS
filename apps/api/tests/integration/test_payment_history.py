from fastapi.testclient import TestClient

from app.main import app
from app.schemas.payment_entry_out import PaymentEntryOut
from app.schemas.payment_history_page import PaymentHistoryPage

client = TestClient(app)
ENTRY = PaymentEntryOut(sku="topup", amount_cents=500, credits=40, status="completed", paid_at=None)
PAGE = PaymentHistoryPage(items=[ENTRY], page=1, page_size=10, total=1, total_pages=1)


def install(monkeypatch):
    asked = []
    monkeypatch.setattr(
        "app.routers.payments.list_payment_history",
        lambda user_id, page, status, product: (
            asked.append((user_id, page, status, product)) or PAGE
        ),
    )
    return asked


def test_returns_a_page_of_the_payment_history_of_the_logged_in_user(monkeypatch, logged_in):
    asked = install(monkeypatch)

    response = client.get("/payments")

    assert response.status_code == 200 and response.json() == PAGE.model_dump()
    assert asked == [("user-1", 1, "all", "all")]


def test_passes_the_page_and_the_filters_on(monkeypatch, logged_in):
    asked = install(monkeypatch)

    client.get("/payments?page=2&status=failed&product=plan")

    assert asked == [("user-1", 2, "failed", "plan")]


def test_an_unknown_filter_value_is_rejected(monkeypatch, logged_in):
    install(monkeypatch)

    assert client.get("/payments?status=pending").status_code == 422


def test_page_zero_is_rejected(monkeypatch, logged_in):
    install(monkeypatch)

    assert client.get("/payments?page=0").status_code == 422
