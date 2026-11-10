import app.services.scans.find_previous_scan as module
from app.schemas.match_result import MatchResult
from app.schemas.verdict import Verdict
from app.services.scans.hash_job_url import hash_job_url

RESULT = MatchResult(
    verdict=Verdict.PASS,
    score=20,
    summary="Not a fit.",
    matching_skills=[],
    missing_skills=[],
    red_flags=[],
)


def test_a_scan_without_a_url_is_never_looked_up(monkeypatch):
    def fail(user_id, url_hash):
        raise AssertionError("must not look anything up")

    monkeypatch.setattr(module, "find_scan_result", fail)

    assert module.find_previous_scan("user-1", None) is None
    assert module.find_previous_scan("user-1", "") is None


def test_looks_up_the_hash_of_the_url_for_this_user(monkeypatch):
    asked = []

    def fake(user_id, url_hash):
        asked.append((user_id, url_hash))
        return RESULT

    monkeypatch.setattr(module, "find_scan_result", fake)

    found = module.find_previous_scan("user-1", "https://example.com/jobs/1?utm_source=x")

    assert found == RESULT
    assert asked == [("user-1", hash_job_url("https://example.com/jobs/1"))]


def test_a_failed_lookup_never_blocks_the_scan(monkeypatch):
    def fail(user_id, url_hash):
        raise RuntimeError("table down")

    monkeypatch.setattr(module, "find_scan_result", fail)

    assert module.find_previous_scan("user-1", "https://example.com/jobs/1") is None
