import pytest
from appwrite.exception import AppwriteException

import app.services.usage.record_scan as module
from app.schemas.match_result import MatchResult
from app.schemas.verdict import Verdict
from app.services.scans.hash_job_url import hash_job_url
from app.types.authenticated_user import AuthenticatedUser
from app.types.scan_savings import ScanSavings

SAVINGS = ScanSavings(minutes=5.0, cash=4.1667)
USER = AuthenticatedUser("user-1", "Jane Doe", "jane.doe@example.com", True, {"jobId": "job-1"})
RESULT = MatchResult(
    verdict=Verdict.SMASH,
    score=80,
    summary="Good fit.",
    matching_skills=[],
    missing_skills=[],
    red_flags=[],
)
JOB_TEXT = "word " * 1125
URL = "https://example.com/job"


@pytest.fixture(autouse=True)
def uses(monkeypatch):
    calls = []
    monkeypatch.setattr(
        module,
        "record_extension_use",
        lambda user_id, install_id, counted: calls.append((user_id, install_id, counted)),
    )
    return calls


def install(monkeypatch, save_error=None, fail_usage=False):
    saved, recorded = [], []

    def save(*args):
        if save_error:
            raise save_error
        saved.append(args)

    def usage(*args):
        if fail_usage:
            raise RuntimeError("usage table down")
        recorded.append(args)

    monkeypatch.setattr(module, "measure_savings", lambda user, words: SAVINGS)
    monkeypatch.setattr(module, "save_scan", save)
    monkeypatch.setattr(module, "record_scan_usage", usage)
    return saved, recorded


def test_saves_the_scan_and_the_totals_with_the_same_measurements(monkeypatch):
    saved, recorded = install(monkeypatch)

    module.record_scan(USER, RESULT, URL, "Dev", JOB_TEXT)

    assert saved == [("user-1", RESULT, URL, "Dev", 1125, SAVINGS, hash_job_url(URL))]
    assert recorded == [("user-1", 1125, SAVINGS)]


def test_a_scan_without_a_url_is_saved_without_a_hash(monkeypatch):
    saved, _ = install(monkeypatch)

    module.record_scan(USER, RESULT, None, None, JOB_TEXT)

    assert saved[0][-1] is None


def test_a_page_recorded_a_moment_ago_adds_nothing_to_the_totals(monkeypatch):
    saved, recorded = install(monkeypatch, save_error=AppwriteException("duplicate", 409))

    module.record_scan(USER, RESULT, URL, "Dev", JOB_TEXT)

    assert saved == [] and recorded == []


def test_a_failing_history_save_still_records_the_totals(monkeypatch):
    saved, recorded = install(monkeypatch, save_error=RuntimeError("scans table down"))

    module.record_scan(USER, RESULT, None, None, JOB_TEXT)

    assert saved == [] and len(recorded) == 1


def test_a_failing_totals_update_still_saves_the_history(monkeypatch):
    saved, recorded = install(monkeypatch, fail_usage=True)

    module.record_scan(USER, RESULT, None, None, JOB_TEXT)

    assert len(saved) == 1 and recorded == []


def test_never_raises_even_when_everything_fails(monkeypatch):
    install(monkeypatch, save_error=RuntimeError("down"), fail_usage=True)

    module.record_scan(USER, RESULT, None, None, JOB_TEXT)


def test_a_scan_made_from_an_extension_counts_for_that_install(monkeypatch, uses):
    install(monkeypatch)

    module.record_scan(USER, RESULT, URL, "Dev", JOB_TEXT, "install-12345678")

    assert uses == [("user-1", "install-12345678", True)]


def test_a_page_recorded_a_moment_ago_does_not_count_for_the_install(monkeypatch, uses):
    install(monkeypatch, save_error=AppwriteException("duplicate", 409))

    module.record_scan(USER, RESULT, URL, "Dev", JOB_TEXT, "install-12345678")

    assert uses == []
