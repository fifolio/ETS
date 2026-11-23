from datetime import datetime

from app.constants.credits import WELCOME_CREDITS
from app.constants.plans import PLANS
from app.services.credits.add_credits import add_credits
from app.services.subscriptions.create_subscription_row import create_subscription_row
from app.services.subscriptions.has_subscription import has_subscription


def ensure_credit_account(user_id: str, now: datetime) -> None:
    """First visit: the welcome bonus and the Explore allowance, each once (by key), then the row.

    The grants come first, so a failure leaves no row and the next call tries again.
    """
    if has_subscription(user_id):
        return
    explore = PLANS[0]  # the lowest plan
    add_credits(user_id, "promotional", WELCOME_CREDITS, "Welcome bonus", f"welcome:{user_id}")
    add_credits(
        user_id,
        "subscription",
        explore.subscription_credits,
        "Explore credits",
        f"explore-init:{user_id}",
    )
    create_subscription_row(user_id, explore.id, now)
