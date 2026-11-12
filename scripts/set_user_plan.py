import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.constants.account import SUBSCRIPTION_PLANS 
from app.services.account.set_user_plan import set_user_plan  


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[2] not in SUBSCRIPTION_PLANS:
        sys.exit(f"Usage: set_user_plan.py <user-id> <{'|'.join(SUBSCRIPTION_PLANS)}>")
    set_user_plan(sys.argv[1], sys.argv[2])
    print(f"User {sys.argv[1]} is now on the {sys.argv[2]} plan.")


if __name__ == "__main__":
    main()