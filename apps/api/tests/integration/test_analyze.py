from fastapi.testclient import TestClient

from app.main import app
from app.schemas.verdict import MatchResult, Verdict

client = TestClient(app)

VALID_PAYLOAD = {
    "cv_text": "Jane Doe, frontend developer. " * 10,
    "job_text": "We are hiring a React developer to build our web app. " * 3,
}

FAKE_RESULT = MatchResult(
    verdict=Verdict.SMASH,
    score=82,
    summary="Strong fit for this role.",
    matching_skills=["React"],
    missing_skills=[],
    red_flags=[],
)


def test_analyze_returns_verdict(monkeypatch):
    monkeypatch.setattr("app.routers.analyze.analyze", lambda cv, job: FAKE_RESULT)
    response = client.post("/analyze", json=VALID_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert body["verdict"] == "smash"
    assert body["score"] == 82


def test_analyze_rejects_short_cv():
    response = client.post("/analyze", json={"cv_text": "Too short"})
    assert response.status_code == 422


def test_analyze_model_failure_returns_502(monkeypatch):
    def boom(cv, job):
        raise ValueError("model exploded")

    monkeypatch.setattr("app.routers.analyze.analyze", boom)
    response = client.post("/analyze", json=VALID_PAYLOAD)
    assert response.status_code == 502


def test_analyze_missing_key_returns_503(monkeypatch):
    def no_key(cv, job):
        raise RuntimeError("AI API KEY service not configured")

    monkeypatch.setattr("app.routers.analyze.analyze", no_key)
    response = client.post("/analyze", json=VALID_PAYLOAD)
    assert response.status_code == 503
