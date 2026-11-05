from datetime import UTC, datetime, timedelta

import pytest

from app.core.config import settings
from app.services.cleanup.is_setup_expired import is_setup_expired
from app.types.account_summary import AccountSummary

NOW = datetime(2026, 11, 10, 12, 0, tzinfo=UTC)


@pytest.fixture(autouse=True)
def forty_eight_hours(monkeypatch):
    monkeypatch.setattr(settings, "setup_deadline_hours", 48)


def make_account(hours_old=49, verified=True, labels=None):
    return AccountSummary("user-1", NOW - timedelta(hours=hours_old), verified, labels or [])


def no_cv(user_id):
    return False


def has_cv(user_id):
    return True


def test_a_young_account_is_never_expired():
    assert is_setup_expired(make_account(hours_old=47, verified=False), NOW, no_cv) is False


def test_an_old_unverified_account_is_expired():
    assert is_setup_expired(make_account(verified=False), NOW, has_cv) is True


def test_an_old_verified_account_with_the_cv_label_is_kept():
    assert is_setup_expired(make_account(labels=["cvdone"]), NOW, no_cv) is False


def test_an_old_verified_account_with_a_stored_cv_is_kept():
    assert is_setup_expired(make_account(), NOW, has_cv) is False


def test_an_old_verified_account_without_any_cv_is_expired():
    assert is_setup_expired(make_account(), NOW, no_cv) is True


def test_the_keep_label_protects_an_account():
    assert (
        is_setup_expired(make_account(verified=False, labels=["keepaccount"]), NOW, no_cv) is False
    )
