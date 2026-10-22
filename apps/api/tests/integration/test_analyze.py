import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.verdict import MatchResult, Verdict
from app.services.cv_store import StoredCV

pytestmark = pytest.mark.usefixtures("logged_in")

client = TestClient(app)

VALID_PAYLOAD = {
    "job_text": "We are hiring a React developer to build our web app. " * 3,
    "job_url": "https://example.com/jobs/1",
    "job_title": "React Developer",
}

FAKE_CV = StoredCV("row-1", "file-1", "cv.pdf", "Jane Doe, frontend developer. " * 10)

FAKE_RESULT = MatchResult(
    verdict=Verdict.SMASH,
    score=82,
    summary="Strong fit for this role.",
    matching_skills=["React"],
    missing_skills=[],
    red_flags=[],
)


@pytest.fixture
def stored_cv(monkeypatch):
    monkeypatch.setattr("app.routers.analyze.get_cv", lambda user_id: FAKE_CV)


def test_analyze_returns_verdict_and_saves_scan(monkeypatch, stored_cv):
    saved = []
    monkeypatch.setattr("app.routers.analyze.analyze", lambda cv, job: FAKE_RESULT)
    monkeypatch.setattr("app.routers.analyze.save_scan", lambda *args: saved.append(args))

    response = client.post("/analyze", json=VALID_PAYLOAD)

    assert response.status_code == 200
    assert response.json()["verdict"] == "smash"
    assert len(saved) == 1
    assert saved[0][0] == "user-1"


def test_analyze_without_cv_returns_404(monkeypatch):
    monkeypatch.setattr("app.routers.analyze.get_cv", lambda user_id: None)
    response = client.post("/analyze", json=VALID_PAYLOAD)
    assert response.status_code == 404


def test_analyze_rejects_short_job_text():
    response = client.post("/analyze", json={"job_text": "too short"})
    assert response.status_code == 422


def test_analyze_model_failure_returns_502(monkeypatch, stored_cv):
    def boom(cv, job):
        raise ValueError("model exploded")

    monkeypatch.setattr("app.routers.analyze.analyze", boom)
    response = client.post("/analyze", json=VALID_PAYLOAD)
    assert response.status_code == 502


def test_analyze_missing_key_returns_503(monkeypatch, stored_cv):
    def no_key(cv, job):
        raise RuntimeError("GROQ_API_KEY is not set")

    monkeypatch.setattr("app.routers.analyze.analyze", no_key)
    response = client.post("/analyze", json=VALID_PAYLOAD)
    assert response.status_code == 503


def test_analyze_still_returns_verdict_if_saving_history_fails(monkeypatch, stored_cv):
    def fail(*args):
        raise ValueError("database down")

    monkeypatch.setattr("app.routers.analyze.analyze", lambda cv, job: FAKE_RESULT)
    monkeypatch.setattr("app.routers.analyze.save_scan", fail)

    response = client.post("/analyze", json=VALID_PAYLOAD)
    assert response.status_code == 200
