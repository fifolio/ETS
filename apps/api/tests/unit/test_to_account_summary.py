from datetime import UTC
from types import SimpleNamespace

from app.services.cleanup.to_account_summary import to_account_summary


def make_user(registration):
    return SimpleNamespace(
        id="user-1", registration=registration, emailverification=True, labels=["nextmove"]
    )


def test_reads_the_fields_of_an_appwrite_user():
    summary = to_account_summary(make_user("2026-11-02T10:00:00.000+00:00"))

    assert summary.id == "user-1"
    assert summary.registered_at.isoformat() == "2026-11-02T10:00:00+00:00"
    assert summary.email_verified is True
    assert summary.labels == ["nextmove"]


def test_a_date_without_a_time_zone_is_treated_as_utc():
    assert to_account_summary(make_user("2026-11-02T10:00:00")).registered_at.tzinfo == UTC
