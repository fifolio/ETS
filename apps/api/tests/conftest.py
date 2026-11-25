from datetime import UTC, datetime

import pytest

from app.dependencies.get_current_user import get_current_user
from app.main import app
from app.types.authenticated_user import AuthenticatedUser
from app.types.payment_notice import PaymentNotice
from app.types.payment_record import PaymentRecord
from app.types.subscription_record import SubscriptionRecord

TEST_USER = AuthenticatedUser(
    id="user-1", name="Jane Doe", email="jane.doe@example.com", email_verified=True
)


@pytest.fixture
def logged_in():
    app.dependency_overrides[get_current_user] = lambda: TEST_USER
    yield TEST_USER
    app.dependency_overrides.clear()


@pytest.fixture
def complete_prefs():
    return {
        "industryId": "software-it",
        "industry": "Software & IT",
        "jobId": "job-1",
        "role": "Software engineer",
        "hourlyRateUsd": 50.0,
        "seniority": "mid",
        "yearsOfExperience": 4,
        "currentLocation": "Tunis, Tunisia",
        "desiredLocations": ["Berlin, Germany"],
        "workArrangements": ["remote", "hybrid"],
        "employmentTypes": ["full-time"],
    }


def make_notice(**overrides):
    values = {
        "provider": "whop",
        "environment": "sandbox",
        "payment_id": "pay_1",
        "checkout_id": "ch_1",
        "user_id": "user-1",
        "sku": "topup",
        "paid_cents": 500,
        "currency": "usd",
        "membership_id": None,
        "customer_id": "mber_1",
        "paid_at": datetime(2026, 12, 1, 10, 0, tzinfo=UTC),
    }
    return PaymentNotice(**{**values, **overrides})


def make_record(**overrides):
    values = {
        "row_id": "row-1",
        "user_id": "user-1",
        "sku": "topup",
        "checkout_id": "ch_1",
        "payment_id": None,
        "amount_cents": 500,
        "credits": 40,
        "status": "pending",
        "applied": False,
    }
    return PaymentRecord(**{**values, **overrides})


def make_subscription(**overrides):
    values = {
        "user_id": "user-1",
        "plan": "nextmove",
        "status": "active",
        "membership_id": "mem_1",
        "cancel_at_period_end": False,
        "period_end": datetime(2026, 12, 31, tzinfo=UTC),
        "credits_renewed_at": datetime(2026, 12, 1, tzinfo=UTC),
        "reminder_sent_at": None,
    }
    return SubscriptionRecord(**{**values, **overrides})
