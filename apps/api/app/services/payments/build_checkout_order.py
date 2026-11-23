from app.constants.topups import TOPUP_SKU
from app.exceptions.checkout_refused_error import CheckoutRefusedError
from app.services.plans.find_plan import find_plan
from app.services.plans.validate_upgrade import validate_upgrade
from app.services.topups.credits_for_cents import credits_for_cents
from app.services.topups.validate_topup_amount import validate_topup_amount
from app.types.authenticated_user import AuthenticatedUser
from app.types.checkout_order import CheckoutOrder


def build_checkout_order(
    user: AuthenticatedUser, product: str, amount_usd: float | None = None
) -> CheckoutOrder:
    """What the user is buying and what it costs. The server decides the price and the credits."""
    if product == TOPUP_SKU:
        cents = validate_topup_amount(amount_usd)
        return CheckoutOrder(user.id, user.email, TOPUP_SKU, cents, credits_for_cents(cents))

    problem = validate_upgrade(user.subscription, product)
    plan = find_plan(product)
    if problem or plan is None:
        raise CheckoutRefusedError(problem or "Unknown product.")
    return CheckoutOrder(
        user.id,
        user.email,
        f"plan_{plan.id}",
        round(plan.price_usd_per_month * 100),
        plan.subscription_credits,
    )
