import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.match_result import MatchResult
from app.schemas.verdict import Verdict
from app.types.stored_cv import StoredCV

pytestmark = pytest.mark.usefixtures("logged_in")

client = TestClient(app)

VALID_PAYLOAD = {
    "job_text": "We are hiring a React developer to build our web app. " * 3,
    "job_url": "https://example.com/jobs/1",
    "job_title": "React Developer",
}

FAKE_CV = StoredCV("row-1", "cv.pdf", "Jane Doe, frontend developer. " * 10)

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


@pytest.fixture(autouse=True)
def nothing_scanned_before(monkeypatch):
    monkeypatch.setattr("app.routers.analyze.find_previous_scan", lambda user_id, url: None)


def test_analyze_returns_the_verdict_and_records_the_scan(monkeypatch, stored_cv):
    recorded = []
    monkeypatch.setattr("app.routers.analyze.analyze", lambda cv, job: FAKE_RESULT)
    monkeypatch.setattr("app.routers.analyze.record_scan", lambda *args: recorded.append(args))

    response = client.post("/analyze", json=VALID_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["verdict"] == "smash"
    assert body["already_scanned"] is False
    user, result, job_url, job_title, job_text = recorded[0]
    assert user.id == "user-1"
    assert result == FAKE_RESULT
    assert (job_url, job_title) == (VALID_PAYLOAD["job_url"], VALID_PAYLOAD["job_title"])
    assert job_text == VALID_PAYLOAD["job_text"]


def test_a_page_scanned_before_returns_the_stored_result_and_counts_nothing(monkeypatch, stored_cv):
    calls = []
    monkeypatch.setattr("app.routers.analyze.find_previous_scan", lambda user_id, url: FAKE_RESULT)
    monkeypatch.setattr("app.routers.analyze.analyze", lambda cv, job: calls.append("analyze"))
    monkeypatch.setattr("app.routers.analyze.record_scan", lambda *args: calls.append("record"))

    response = client.post("/analyze", json=VALID_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["already_scanned"] is True
    assert (body["verdict"], body["score"]) == ("smash", 82)
    assert calls == []  # no AI call and nothing recorded


def test_the_previous_scan_check_uses_the_user_and_the_url_of_the_request(monkeypatch, stored_cv):
    asked = []

    def fake_lookup(user_id, url):
        asked.append((user_id, url))
        return FAKE_RESULT

    monkeypatch.setattr("app.routers.analyze.find_previous_scan", fake_lookup)

    client.post("/analyze", json=VALID_PAYLOAD)

    assert asked == [("user-1", "https://example.com/jobs/1")]


def test_analyze_without_cv_returns_404(monkeypatch):
    monkeypatch.setattr("app.routers.analyze.get_cv", lambda user_id: None)
    assert client.post("/analyze", json=VALID_PAYLOAD).status_code == 404


def test_analyze_rejects_short_job_text():
    assert client.post("/analyze", json={"job_text": "too short"}).status_code == 422


def test_analyze_model_failure_returns_502(monkeypatch, stored_cv):
    def boom(cv, job):
        raise ValueError("model exploded")

    monkeypatch.setattr("app.routers.analyze.analyze", boom)
    assert client.post("/analyze", json=VALID_PAYLOAD).status_code == 502


def test_analyze_missing_key_returns_503(monkeypatch, stored_cv):
    def no_key(cv, job):
        raise RuntimeError("GROQ_API_KEY is not set")

    monkeypatch.setattr("app.routers.analyze.analyze", no_key)
    assert client.post("/analyze", json=VALID_PAYLOAD).status_code == 503
