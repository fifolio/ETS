import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.core.config import settings 
from app.services.appwrite.get_tables_db import get_tables_db  
from app.services.payments.whop.whop_provider import WhopProvider  
from app.services.topups.credits_for_cents import credits_for_cents  
from app.types.checkout_order import CheckoutOrder  

PROBLEMS: list[str] = []
TABLES = ("payments", "subscriptions", "credit_balances", "credit_ledger")


def report(ok: bool, label: str, hint: str = "") -> None:
    print(("OK   " if ok else "FAIL ") + label + ("" if ok else f"  -> {hint}"))
    if not ok:
        PROBLEMS.append(label)


def main() -> None:
    env = settings.whop_environment
    report(env in ("sandbox", "production"), f"WHOP_ENVIRONMENT is {env}", "use sandbox or production")
    report(settings.payment_provider == "whop", "PAYMENT_PROVIDER is whop", "set PAYMENT_PROVIDER=whop")
    if env not in ("sandbox", "production"):
        sys.exit(1)
    other = "production" if env == "sandbox" else "sandbox"

    def value(environment: str, name: str) -> str:
        return getattr(settings, f"whop_{environment}_{name}")

    needed = ("api_key", "webhook_secret", "plan_nextmove", "plan_urgent", "product_topup")
    for name in needed:
        report(bool(value(env, name)), f"{env}: {name} is set", f"set WHOP_{env.upper()}_{name.upper()}")
    for name in needed:
        same = bool(value(env, name)) and value(env, name) == value(other, name)
        report(not same, f"{name} differs between sandbox and production", "the same value is used for both")

    url = settings.payment_success_url
    if env == "production":
        report(url.startswith("https://") and "localhost" not in url, "PAYMENT_SUCCESS_URL is the real https address", url)
    report(bool(settings.cleanup_token), "CLEANUP_TOKEN is set (scheduled maintenance)", "set CLEANUP_TOKEN")

    for table in TABLES:
        try:
            get_tables_db().list_rows(
                database_id=settings.appwrite_database_id, table_id=getattr(settings, f"appwrite_{table}_table_id")
            )
            report(True, f"Appwrite table {table} is reachable")
        except Exception as exc:
            report(False, f"Appwrite table {table} is reachable", str(exc))

    if "--live" in sys.argv:
        print(f"\nCreating one unpaid checkout per product in the {env} environment...")
        for sku, cents in (("plan_nextmove", 700), ("plan_urgent", 1400), ("topup", 300)):
            credits = credits_for_cents(cents) if sku == "topup" else 0
            try:
                session = WhopProvider().create_checkout(
                    CheckoutOrder("preflight", "preflight@example.com", sku, cents, credits)
                )
                report(True, f"{sku}: Whop created a checkout")
                print("      ", session.url)
            except Exception as exc:
                report(False, f"{sku}: Whop created a checkout", str(exc))
    else:
        print("\n(Add --live to also create an unpaid checkout for each product.)")

    print("\nAll checks passed." if not PROBLEMS else f"\n{len(PROBLEMS)} problem(s) to fix.")
    sys.exit(1 if PROBLEMS else 0)


if __name__ == "__main__":
    main()