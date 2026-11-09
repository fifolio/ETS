import app.services.usage.record_scan as module

from app.schemas.match_result import MatchResult
from app.schemas.verdict import Verdict
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


def install(monkeypatch, fail_save=False, fail_usage=False):
    saved, recorded = [], []

    def save(*args):
        if fail_save:
            raise RuntimeError("scans table down")
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

    module.record_scan(USER, RESULT, "https://example.com/job", "Dev", JOB_TEXT)

    assert saved == [("user-1", RESULT, "https://example.com/job", "Dev", 1125, SAVINGS)]
    assert recorded == [("user-1", 1125, SAVINGS)]


def test_a_failing_history_save_still_records_the_totals(monkeypatch):
    saved, recorded = install(monkeypatch, fail_save=True)

    module.record_scan(USER, RESULT, None, None, JOB_TEXT)

    assert saved == [] and len(recorded) == 1


def test_a_failing_totals_update_still_saves_the_history(monkeypatch):
    saved, recorded = install(monkeypatch, fail_usage=True)

    module.record_scan(USER, RESULT, None, None, JOB_TEXT)

    assert len(saved) == 1 and recorded == []


def test_never_raises_even_when_everything_fails(monkeypatch):
    install(monkeypatch, fail_save=True, fail_usage=True)

    module.record_scan(USER, RESULT, None, None, JOB_TEXT)
