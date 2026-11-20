from dataclasses import dataclass


@dataclass(frozen=True)
class PlanDefinition:
    id: str
    name: str
    price_usd_per_month: float
    subscription_credits: int  # the monthly allowance
    promotional_credits: int  # one-time bonus for a new subscriber
    topup_price_usd: float  # price of one top-up at this plan
    topup_credits: int = 25  # credits in one top-up
