from dataclasses import dataclass


@dataclass(frozen=True)
class CheckoutOrder:
    user_id: str
    email: str
    sku: str  # plan_nextmove, plan_urgent, or topup
    amount_cents: int  # what the server says it costs
    credits: int = 0  # the credits this purchase adds (monthly allowance, or the top-up)
