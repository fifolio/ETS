from datetime import UTC, datetime

from app.exceptions.subscription_action_error import SubscriptionActionError
from app.schemas.subscription_out import SubscriptionOut
from app.services.payments.end_subscription import end_subscription
from app.services.payments.get_payment_provider import get_payment_provider
from app.services.subscriptions.build_subscription_status import build_subscription_status
from app.services.subscriptions.find_subscription_row import find_subscription_row
from app.types.authenticated_user import AuthenticatedUser


def cancel_user_subscription(user: AuthenticatedUser) -> SubscriptionOut:
    """End the subscription and its paid access immediately."""
    record = find_subscription_row("$id", user.id)
    status = build_subscription_status(user.subscription, record)
    if status.cancel_at_period_end:
        return status  # already cancelled: nothing to do
    if not status.can_cancel or record is None or not record.membership_id:
        raise SubscriptionActionError("You have no paid subscription to cancel.", 400)

    get_payment_provider().cancel_subscription(record.membership_id)
    current_record = find_subscription_row("$id", user.id)
    if current_record and current_record.membership_id == record.membership_id:
        end_subscription(current_record, datetime.now(UTC))
        return build_subscription_status("explore", None)
    if current_record and current_record.membership_id:
        return build_subscription_status(current_record.plan, current_record)
    return build_subscription_status("explore", None)
