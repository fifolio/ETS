from fastapi.testclient import TestClient

from app.main import app
from app.schemas.credit_entry_out import CreditEntryOut
from app.schemas.credit_history_page import CreditHistoryPage

client = TestClient(app)
ENTRY = CreditEntryOut(amount=-1, kind="subscription", reason="Job scan", created_at=None)
PAGE = CreditHistoryPage(items=[ENTRY], page=1, page_size=10, total=1, total_pages=1)


def install(monkeypatch):
    asked = []
    monkeypatch.setattr(
        "app.routers.credit_history.list_credit_history",
        lambda user_id, page, kind, change: asked.append((user_id, page, kind, change)) or PAGE,
    )
    return asked


def test_returns_a_page_of_the_credit_history_of_the_logged_in_user(monkeypatch, logged_in):
    asked = install(monkeypatch)

    response = client.get("/credits/history")

    assert response.status_code == 200 and response.json() == PAGE.model_dump()
    assert asked == [("user-1", 1, "all", "all")]


def test_passes_the_page_and_the_filters_on(monkeypatch, logged_in):
    asked = install(monkeypatch)

    client.get("/credits/history?page=3&kind=purchased&change=used")

    assert asked == [("user-1", 3, "purchased", "used")]


def test_an_unknown_filter_value_is_rejected(monkeypatch, logged_in):
    install(monkeypatch)

    assert client.get("/credits/history?kind=gift").status_code == 422


def test_page_zero_is_rejected(monkeypatch, logged_in):
    install(monkeypatch)

    assert client.get("/credits/history?page=0").status_code == 422
