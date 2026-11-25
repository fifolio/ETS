from datetime import datetime

from app.schemas.maintenance_result import MaintenanceResult
from app.services.cleanup.apply_to_each import apply_to_each
from app.services.payments.end_subscription import end_subscription
from app.services.subscriptions.list_due_explore_renewals import list_due_explore_renewals
from app.services.subscriptions.list_expired_paid_subscriptions import (
    list_expired_paid_subscriptions,
)
from app.services.subscriptions.list_renewal_reminders import list_renewal_reminders
from app.services.subscriptions.renew_explore_credits import renew_explore_credits
from app.services.subscriptions.send_renewal_reminder import send_renewal_reminder


def run_subscription_maintenance(now: datetime, dry_run: bool) -> MaintenanceResult:
    """Explore's monthly reset, the expiry safety net, and the renewal reminders."""
    renewals = list_due_explore_renewals(now)
    expired = list_expired_paid_subscriptions(now)
    reminders = list_renewal_reminders(now)

    renewed = ended = reminded = failed = 0
    if not dry_run:
        renewed, f1 = apply_to_each(renewals, lambda record: renew_explore_credits(record, now))
        ended, f2 = apply_to_each(expired, lambda record: end_subscription(record, now))
        reminded, f3 = apply_to_each(reminders, lambda record: send_renewal_reminder(record, now))
        failed = f1 + f2 + f3
    return MaintenanceResult(
        explore_renewals_due=len(renewals),
        expired_due=len(expired),
        reminders_due=len(reminders),
        explore_renewed=renewed,
        ended=ended,
        reminded=reminded,
        failed=failed,
        dry_run=dry_run,
    )
