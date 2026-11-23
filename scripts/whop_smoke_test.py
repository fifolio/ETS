import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.services.payments.whop.whop_provider import WhopProvider  
from app.types.checkout_order import CheckoutOrder 
from app.services.topups.credits_for_cents import credits_for_cents  # noqa: E402


def main() -> None:
    sku = sys.argv[1] if len(sys.argv) > 1 else "plan_nextmove"
    cents = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    credits = credits_for_cents(cents) if sku == "topup" else 0
    order = CheckoutOrder("smoke-test-user", "smoke@example.com", sku, cents, credits)
    print(WhopProvider().create_checkout(order))


if __name__ == "__main__":
    main()