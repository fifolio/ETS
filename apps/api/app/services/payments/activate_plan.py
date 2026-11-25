from datetime import datetime, timedelta

from app.services.account.set_user_plan import set_user_plan
from app.services.credits.apply_plan_credits import apply_plan_credits
from app.services.payments.cancel_replaced_membership import cancel_replaced_membership
from app.services.subscriptions.find_subscription_row import find_subscription_row
from app.services.subscriptions.update_subscription_row import update_subscription_row
from app.types.payment_notice import PaymentNotice

PROVISIONAL_PERIOD_DAYS = 30  # a new plan is provisionally active for this long, until the provider confirms the first payment


def activate_plan(notice: PaymentNotice, plan_id: str, now: datetime) -> None:
    """Move the user to the plan they paid for (first payment, renewal, or upgrade).

    Safe to repeat for the same payment.
    """
    current = find_subscription_row("$id", notice.user_id)
    period_start = notice.paid_at or now
    update_subscription_row(
        notice.user_id,
        {
            "plan": plan_id,
            "status": "active",
            "provider": notice.provider,
            "providerSubscriptionId": notice.membership_id,
            "providerCustomerId": notice.customer_id,
            "cancelAtPeriodEnd": False,
            "currentPeriodEnd": (
                period_start + timedelta(days=PROVISIONAL_PERIOD_DAYS)
            ).isoformat(),
            "creditsRenewedAt": now.isoformat(),
            "renewalReminderSentAt": None,
        },
    )
    set_user_plan(notice.user_id, plan_id)
    apply_plan_credits(notice.user_id, plan_id, notice.payment_id)
    if (
        current is not None
        and current.membership_id
        and notice.membership_id
        and current.membership_id != notice.membership_id
    ):
        cancel_replaced_membership(current.membership_id)  # an upgrade: don't bill both
