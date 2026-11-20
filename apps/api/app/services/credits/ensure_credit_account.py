from datetime import datetime

from app.constants.plans import PLANS
from app.services.credits.add_credits import add_credits
from app.services.credits.read_credit_balance import get_credit_balance
from app.services.subscriptions.create_subscription_row import create_subscription_row


def ensure_credit_account(user_id: str, now: datetime) -> None:
    """First visit: create the Explore subscription row and grant the Explore credits, once."""
    if get_credit_balance(user_id) is not None:
        return
    explore = PLANS[0]  # the lowest plan
    create_subscription_row(user_id, explore.id, now)
    add_credits(
        user_id,
        "subscription",
        explore.subscription_credits,
        "Explore credits",
        f"explore-init:{user_id}",
    )
