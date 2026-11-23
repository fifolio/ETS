import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.constants.plans import PLANS  
from app.constants.topups import TOPUP_MAX_CENTS, TOPUP_MIN_CENTS  
from app.services.topups.credits_for_cents import credits_for_cents  

# Assumptions
FEE_PERCENT = 0.027  # Whop domestic card fee
FEE_FIXED_USD = 0.40  # $0.30 + $0.03 (3D Secure) + $0.07 (Radar), the worst case
AI_COST_PER_CREDIT_USD = 0.002  # ESTIMATE


def show(label: str, price: float, credits: int) -> None:
    fee = price * FEE_PERCENT + FEE_FIXED_USD
    ai_cost = credits * AI_COST_PER_CREDIT_USD
    margin = (price - fee - ai_cost) / price
    break_even = (price - fee) / credits
    print(
        f"{label:<12} ${price:>6.2f} {credits:>4} credits ${price / credits:.4f}/credit "
        f"fees ${fee:.2f} AI ${ai_cost:.2f} margin {margin:6.1%} AI break-even ${break_even:.4f}/credit"
    )


def main() -> None:
    print("Subscriptions (every monthly credit used)")
    for plan in PLANS:
        if plan.price_usd_per_month > 0:
            show(plan.name, plan.price_usd_per_month, plan.subscription_credits)
    print("\nTop-ups")
    for cents in (TOPUP_MIN_CENTS, 200, 500, 1000, 2000, TOPUP_MAX_CENTS):
        show("Top-up", cents / 100, credits_for_cents(cents))


if __name__ == "__main__":
    main()