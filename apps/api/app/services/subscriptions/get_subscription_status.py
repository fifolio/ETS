from app.schemas.subscription_out import SubscriptionOut
from app.services.subscriptions.build_subscription_status import build_subscription_status
from app.services.subscriptions.find_subscription_row import find_subscription_row
from app.types.authenticated_user import AuthenticatedUser


def get_subscription_status(user: AuthenticatedUser) -> SubscriptionOut:
    return build_subscription_status(user.subscription, find_subscription_row("$id", user.id))
