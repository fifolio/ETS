from datetime import datetime, timedelta

from app.services.account.set_user_plan import set_user_plan
from app.services.credits.apply_plan_credits import apply_plan_credits
from app.services.subscriptions.update_subscription_row import update_subscription_row
from app.types.payment_notice import PaymentNotice

PROVISIONAL_PERIOD_DAYS = 30


def activate_plan(notice: PaymentNotice, plan_id: str, now: datetime) -> None:
    """Move the user to the plan they paid for. Safe to repeat for the same payment."""
    started = notice.paid_at or now
    set_user_plan(notice.user_id, plan_id)
    update_subscription_row(
        notice.user_id,
        {
            "plan": plan_id,
            "status": "active",
            "provider": notice.provider,
            "providerSubscriptionId": notice.membership_id,
            "providerCustomerId": notice.customer_id,
            "cancelAtPeriodEnd": False,
            "startedAt": started.isoformat(),
            "currentPeriodEnd": (started + timedelta(days=PROVISIONAL_PERIOD_DAYS)).isoformat(),
            "creditsRenewedAt": now.isoformat(),
            "renewalReminderSentAt": None,
        },
    )
    apply_plan_credits(notice.user_id, plan_id, notice.payment_id)
