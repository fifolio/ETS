from app.exceptions.subscription_action_error import SubscriptionActionError
from app.services.payments.get_payment_provider import get_payment_provider
from app.services.subscriptions.find_subscription_row import find_subscription_row
from app.types.authenticated_user import AuthenticatedUser


def get_user_manage_url(user: AuthenticatedUser) -> str:
    """The provider's billing page for the user's subscription."""
    record = find_subscription_row("$id", user.id)
    if user.subscription == "explore" or record is None or not record.membership_id:
        raise SubscriptionActionError("You have no paid subscription.", 404)
    url = get_payment_provider().get_manage_url(record.membership_id)
    if not url:
        raise SubscriptionActionError("The billing page isn't available.", 404)
    return url
