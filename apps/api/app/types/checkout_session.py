from dataclasses import dataclass


@dataclass(frozen=True)
class CheckoutSession:
    checkout_id: str  # the provider's ID for this checkout
    plan_id: str  # the provider's plan being bought
    url: str  # the provider's hosted payment page
