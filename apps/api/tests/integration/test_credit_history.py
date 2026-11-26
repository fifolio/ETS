from fastapi.testclient import TestClient

from app.main import app
from app.schemas.credit_entry_out import CreditEntryOut

client = TestClient(app)


def test_returns_the_credit_history_of_the_logged_in_user(monkeypatch, logged_in):
    asked = []
    entry = CreditEntryOut(amount=-1, kind="subscription", reason="Job scan", created_at=None)
    monkeypatch.setattr(
        "app.routers.credit_history.list_credit_history",
        lambda user_id: asked.append(user_id) or [entry],
    )

    response = client.get("/credits/history")

    assert response.status_code == 200 and response.json() == [entry.model_dump()]
    assert asked == ["user-1"]
