from datetime import datetime

from app.constants.plans import PLANS
from app.services.credits.add_credits import add_credits
from app.services.subscriptions.create_subscription_row import create_subscription_row
from app.services.subscriptions.has_subscription import has_subscription


def ensure_credit_account(user_id: str, now: datetime) -> None:
    """First visit: grant the Explore credits (once, by key) and create the subscription row.

    The grant comes first, so a failure leaves no row and the next call tries again.
    """
    if has_subscription(user_id):
        return
    explore = PLANS[0]  # the lowest plan
    add_credits(
        user_id,
        "subscription",
        explore.subscription_credits,
        "Explore credits",
        f"explore-init:{user_id}",
    )
    create_subscription_row(user_id, explore.id, now)
