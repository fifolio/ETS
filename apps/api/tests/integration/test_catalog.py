from fastapi.testclient import TestClient

from app.main import app
from app.schemas.public_industry import PublicIndustry
from app.schemas.public_job import PublicJob

client = TestClient(app)


def test_industries_are_public_and_cached(monkeypatch):
    monkeypatch.setattr(
        "app.routers.catalog.industries.list_industries",
        lambda: [PublicIndustry(id="marketing", name="Marketing & Advertising")],
    )

    response = client.get("/industries")

    assert response.status_code == 200
    assert response.json() == [{"id": "marketing", "name": "Marketing & Advertising"}]
    assert "max-age" in response.headers["cache-control"]


def test_the_jobs_of_an_industry_are_public_and_include_their_rates(monkeypatch):
    asked = []

    def fake_jobs(industry_id):
        asked.append(industry_id)
        return [PublicJob(id="job-1", name="Financial Analyst", hourly_rate_usd=45.0)]

    monkeypatch.setattr("app.routers.catalog.industry_jobs.list_industry_jobs", fake_jobs)

    response = client.get("/industries/accounting-finance/jobs")

    assert response.status_code == 200
    assert response.json()[0] == {
        "id": "job-1",
        "name": "Financial Analyst",
        "hourly_rate_usd": 45.0,
    }
    assert asked == ["accounting-finance"]


def test_an_industry_without_jobs_returns_an_empty_list(monkeypatch):
    monkeypatch.setattr(
        "app.routers.catalog.industry_jobs.list_industry_jobs", lambda industry_id: []
    )

    assert client.get("/industries/unknown/jobs").json() == []


def test_the_industry_id_is_length_limited():
    assert client.get(f"/industries/{'x' * 65}/jobs").status_code == 422
