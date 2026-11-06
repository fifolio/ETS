from datetime import UTC, datetime, timedelta

import pytest

from app.core.config import settings
from app.services.feedback.is_trial_over import is_trial_over

REGISTERED = datetime(2026, 11, 1, 12, 0, tzinfo=UTC)


@pytest.fixture(autouse=True)
def fifteen_days(monkeypatch):
    monkeypatch.setattr(settings, "feedback_min_days", 15)


def test_the_trial_is_over_after_exactly_fifteen_days():
    assert is_trial_over(REGISTERED, REGISTERED + timedelta(days=15)) is True


def test_the_trial_is_not_over_a_minute_early():
    assert (
        is_trial_over(REGISTERED, REGISTERED + timedelta(days=15) - timedelta(minutes=1)) is False
    )


def test_an_unknown_sign_up_date_never_counts_as_over():
    assert is_trial_over(None, REGISTERED + timedelta(days=100)) is False
