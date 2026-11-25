from app.schemas.subscription_row import SubscriptionRow
from app.services.appwrite.parse_optional_datetime import parse_optional_datetime
from app.types.subscription_record import SubscriptionRecord


def to_subscription_record(row_id: str, row: SubscriptionRow) -> SubscriptionRecord:
    return SubscriptionRecord(
        user_id=row_id,
        plan=row.plan,
        status=row.status,
        membership_id=row.providerSubscriptionId or None,
        cancel_at_period_end=row.cancelAtPeriodEnd,
        period_end=parse_optional_datetime(row.currentPeriodEnd),
        credits_renewed_at=parse_optional_datetime(row.creditsRenewedAt),
        reminder_sent_at=parse_optional_datetime(row.renewalReminderSentAt),
    )
