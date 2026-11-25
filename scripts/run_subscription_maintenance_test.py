import argparse
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import httpx
from appwrite.query import Query
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.core.config import settings
from app.services.account.set_user_plan import set_user_plan
from app.services.appwrite.get_tables_db import get_tables_db
from app.services.appwrite.get_users import get_users
from app.services.credits.read_credit_balance import get_credit_balance
from app.services.subscriptions.find_subscription_row import find_subscription_row
from app.services.subscriptions.list_due_explore_renewals import (
    list_due_explore_renewals,
)
from app.services.subscriptions.list_expired_paid_subscriptions import (
    list_expired_paid_subscriptions,
)
from app.services.subscriptions.list_renewal_reminders import (
    list_renewal_reminders,
)
from app.services.subscriptions.update_subscription_row import (
    update_subscription_row,
)

EXPECTED_COUNTS = {"explore_renewals_due": 1, "expired_due": 1, "reminders_due": 1}


class LedgerKeyRow(BaseModel):
    idempotencyKey: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare three disposable Appwrite users, verify maintenance in dry-run mode, "
            "and optionally apply it."
        )
    )
    parser.add_argument("--explore-user-id", required=True)
    parser.add_argument("--expired-user-id", required=True)
    parser.add_argument("--reminder-user-id", required=True)
    parser.add_argument("--api-url", default="http://127.0.0.1:8000")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the test dates and run maintenance after a successful dry run.",
    )
    return parser.parse_args()


def require_test_accounts(user_ids: dict[str, str]) -> None:
    if len(set(user_ids.values())) != len(user_ids):
        raise ValueError("Provide three different test user IDs.")

    users = get_users()
    for role, user_id in user_ids.items():
        users.get(user_id=user_id)
        record = find_subscription_row("$id", user_id)
        if record is None:
            raise ValueError(f"The {role} user has no subscription row.")
        if record.membership_id:
            raise ValueError(
                f"The {role} user has a provider membership attached; refusing to alter it."
            )
        if role == "explore" and record.plan != "explore":
            raise ValueError("The Explore test user must already be on Explore.")


def prepare_accounts(user_ids: dict[str, str], now: datetime) -> None:
    updates = {
        "explore": {
            "plan": "explore",
            "status": "active",
            "providerSubscriptionId": None,
            "cancelAtPeriodEnd": False,
            "currentPeriodEnd": None,
            "creditsRenewedAt": (now - timedelta(days=40)).isoformat(),
            "renewalReminderSentAt": None,
        },
        "expired": {
            "plan": "nextmove",
            "status": "active",
            "providerSubscriptionId": None,
            "cancelAtPeriodEnd": False,
            "currentPeriodEnd": (now - timedelta(days=10)).isoformat(),
            "renewalReminderSentAt": None,
        },
        "reminder": {
            "plan": "nextmove",
            "status": "active",
            "providerSubscriptionId": None,
            "cancelAtPeriodEnd": False,
            "currentPeriodEnd": (now + timedelta(hours=12)).isoformat(),
            "renewalReminderSentAt": None,
        },
    }

    for role in ("explore", "expired", "reminder"):
        user_id = user_ids[role]
        update_subscription_row(user_id, updates[role])
        set_user_plan(user_id, updates[role]["plan"])


def check_idempotency_keys_are_unused(user_ids: dict[str, str], now: datetime) -> None:
    keys = (
        f"plan-credits:{user_ids['explore']}:explore:explore:{now.date().isoformat()}:expire",
        f"plan-credits:{user_ids['explore']}:explore:explore:{now.date().isoformat()}:grant",
        f"plan-credits:{user_ids['expired']}:explore:end:{user_ids['expired']}:expire",
        f"plan-credits:{user_ids['expired']}:explore:end:{user_ids['expired']}:grant",
    )
    for key in keys:
        result = get_tables_db().list_rows(
            database_id=settings.appwrite_database_id,
            table_id=settings.appwrite_credit_ledger_table_id,
            queries=[Query.equal("idempotencyKey", key), Query.limit(1)],
            model_type=LedgerKeyRow,
        )
        if result.rows:
            raise RuntimeError(
                "A test account already used a maintenance credit key; "
                "use fresh disposable test accounts."
            )


def check_targets_are_only_due(user_ids: dict[str, str], now: datetime) -> None:
    due_users = {
        "explore_renewals_due": {
            record.user_id for record in list_due_explore_renewals(now)
        },
        "expired_due": {
            record.user_id for record in list_expired_paid_subscriptions(now)
        },
        "reminders_due": {record.user_id for record in list_renewal_reminders(now)},
    }
    expected_users = {
        "explore_renewals_due": {user_ids["explore"]},
        "expired_due": {user_ids["expired"]},
        "reminders_due": {user_ids["reminder"]},
    }
    for category, expected in expected_users.items():
        if due_users[category] != expected:
            raise RuntimeError(
                f"{category} includes unexpected rows; refusing to run maintenance."
            )


def call_maintenance(api_url: str, cleanup_token: str, dry_run: bool) -> dict[str, Any]:
    response = httpx.post(
        f"{api_url.rstrip('/')}/internal/subscription-maintenance",
        headers={"X-Cleanup-Token": cleanup_token},
        params={"dry_run": str(dry_run).lower()},
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    if not isinstance(result, dict):
        raise TypeError("Maintenance endpoint returned an unexpected response.")
    return result


def check_expected_counts(result: dict[str, Any]) -> None:
    counts = {key: result.get(key) for key in EXPECTED_COUNTS}
    if counts != EXPECTED_COUNTS:
        raise RuntimeError(
            f"Expected dry-run counts {EXPECTED_COUNTS}, got {counts}; "
            "maintenance was not applied."
        )


def verify_results(user_ids: dict[str, str]) -> None:
    explore = find_subscription_row("$id", user_ids["explore"])
    expired = find_subscription_row("$id", user_ids["expired"])
    reminder = find_subscription_row("$id", user_ids["reminder"])
    explore_balance = get_credit_balance(user_ids["explore"])
    expired_balance = get_credit_balance(user_ids["expired"])

    if explore is None or explore.credits_renewed_at is None:
        raise RuntimeError("Explore renewal did not update its subscription row.")
    if explore_balance is None or explore_balance.subscription != 15:
        raise RuntimeError("Explore test account does not have 15 monthly credits.")
    if (
        expired is None
        or expired.plan != "explore"
        or expired.membership_id is not None
    ):
        raise RuntimeError("Expired paid test account did not return to Explore.")
    if expired_balance is None or expired_balance.subscription != 15:
        raise RuntimeError("Expired test account does not have 15 Explore credits.")
    if reminder is None or reminder.reminder_sent_at is None:
        raise RuntimeError("Renewal reminder timestamp was not saved.")


def main() -> None:
    args = parse_args()
    if not settings.cleanup_token:
        raise ValueError("CLEANUP_TOKEN must be configured in the API environment.")

    user_ids = {
        "explore": args.explore_user_id,
        "expired": args.expired_user_id,
        "reminder": args.reminder_user_id,
    }
    require_test_accounts(user_ids)
    api_url = args.api_url.rstrip("/")
    health = httpx.get(f"{api_url}/health", timeout=10)
    health.raise_for_status()

    if not args.apply:
        print("Preflight passed. No Appwrite rows or balances were changed.")
        print("Rerun with --apply to prepare the test rows and run maintenance.")
        return

    now = datetime.now(UTC)
    check_idempotency_keys_are_unused(user_ids, now)
    prepare_accounts(user_ids, now)
    check_targets_are_only_due(user_ids, datetime.now(UTC))

    dry_run_result = call_maintenance(api_url, settings.cleanup_token, dry_run=True)
    check_expected_counts(dry_run_result)
    print(f"Dry run confirmed: {EXPECTED_COUNTS}")

    applied_result = call_maintenance(api_url, settings.cleanup_token, dry_run=False)
    check_expected_counts(applied_result)
    if any(
        applied_result.get(key) != 1 for key in ("explore_renewed", "ended", "reminded")
    ):
        raise RuntimeError(
            f"Maintenance did not process each test row: {applied_result}"
        )
    if applied_result.get("failed") != 0:
        raise RuntimeError(f"Maintenance reported failures: {applied_result}")

    verify_results(user_ids)
    print(f"Maintenance applied and verified: {applied_result}")
    print("Check the API server log for the subscription_renewing notification line.")


if __name__ == "__main__":
    main()
