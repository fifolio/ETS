from datetime import UTC, datetime
from types import SimpleNamespace

from app.services.appwrite.read_created_at import read_created_at


def test_reads_the_text_form():
    assert (
        read_created_at(SimpleNamespace(created_at="2026-12-01T10:00:00+00:00"))
        == "2026-12-01T10:00:00+00:00"
    )


def test_turns_a_datetime_into_text():
    row = SimpleNamespace(created_at=datetime(2026, 12, 1, 10, tzinfo=UTC))

    assert read_created_at(row) == "2026-12-01T10:00:00+00:00"


def test_a_row_without_a_creation_time_gives_none():
    assert read_created_at(SimpleNamespace()) is None
