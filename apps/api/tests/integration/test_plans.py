from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.types.job_board import JobBoard

client = TestClient(app)

BOARDS = [
    JobBoard("linkedin", "LinkedIn", "https://www.linkedin.com/jobs", "explore"),
    JobBoard("indeed", "Indeed", "https://www.indeed.com", "nextmove"),
]


def test_the_plans_are_public_with_their_job_board_counts(monkeypatch):
    monkeypatch.setattr(settings, "payment_provider", "none")
    monkeypatch.setattr("app.routers.plans.list_active_job_boards", lambda: BOARDS)

    response = client.get("/plans")

    assert response.status_code == 200
    body = response.json()
    assert [plan["id"] for plan in body["plans"]] == ["explore", "nextmove", "urgent"]
    assert [plan["job_board_count"] for plan in body["plans"]] == [1, 2, 2]
    assert body["payments_enabled"] is False


def test_each_plan_shows_its_price_and_credits_and_the_top_up_rules_come_from_the_server(
    monkeypatch,
):
    monkeypatch.setattr("app.routers.plans.list_active_job_boards", lambda: BOARDS)

    body = client.get("/plans").json()

    assert [(p["id"], p["price_usd_per_month"], p["monthly_credits"]) for p in body["plans"]] == [
        ("explore", 0.0, 15),
        ("nextmove", 7.0, 150),
        ("urgent", 14.0, 300),
    ]
    assert body["topup"] == {
        "min_usd": 3.0,
        "max_usd": 50.0,
        "step_usd": 0.25,
        "credits_per_step": 2,
        "credits_per_usd": 8,
    }


def test_the_plans_can_be_cached(monkeypatch):
    monkeypatch.setattr("app.routers.plans.list_active_job_boards", lambda: BOARDS)

    assert "max-age=60" in client.get("/plans").headers["cache-control"]
