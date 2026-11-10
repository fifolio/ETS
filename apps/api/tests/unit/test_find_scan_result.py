from types import SimpleNamespace

import app.services.scans.find_scan_result as module
from app.schemas.match_result import MatchResult
from app.schemas.verdict import Verdict

RESULT = MatchResult(
    verdict=Verdict.SMASH,
    score=82,
    summary="Strong fit.",
    matching_skills=["React"],
    missing_skills=[],
    red_flags=[],
)


class FakeTables:
    def __init__(self, rows):
        self.rows = rows

    def list_rows(self, **kwargs):
        return SimpleNamespace(rows=self.rows)


def stored(result_json):
    return SimpleNamespace(data=SimpleNamespace(resultJson=result_json))


def test_returns_the_stored_result(monkeypatch):
    monkeypatch.setattr(
        module, "get_tables_db", lambda: FakeTables([stored(RESULT.model_dump_json())])
    )

    assert module.find_scan_result("user-1", "hash") == RESULT


def test_returns_none_when_the_page_was_never_scanned(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([]))

    assert module.find_scan_result("user-1", "hash") is None


def test_returns_none_when_the_stored_result_is_unreadable(monkeypatch):
    monkeypatch.setattr(module, "get_tables_db", lambda: FakeTables([stored("not json")]))

    assert module.find_scan_result("user-1", "hash") is None
