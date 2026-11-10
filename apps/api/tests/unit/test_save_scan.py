import app.services.scans.save_scan as module
from app.schemas.match_result import MatchResult
from app.schemas.verdict import Verdict
from app.types.scan_savings import ScanSavings


class FakeTables:
    def __init__(self):
        self.calls = []

    def create_row(self, **kwargs):
        self.calls.append(kwargs)


def test_stores_the_word_count_the_minutes_and_the_cash(monkeypatch):
    tables = FakeTables()
    monkeypatch.setattr(module, "get_tables_db", lambda: tables)
    result = MatchResult(
        verdict=Verdict.PASS,
        score=30,
        summary="Not a fit.",
        matching_skills=[],
        missing_skills=[],
        red_flags=[],
    )

    module.save_scan(
        "user-1", result, "https://example.com", "Dev", 900, ScanSavings(4.0, 3.3333), "abc123"
    )

    data = tables.calls[0]["data"]
    assert (data["wordCount"], data["minutesSaved"], data["cashEquivalent"]) == (900, 4.0, 3.3333)
    assert data["urlHash"] == "abc123"
