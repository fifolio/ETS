import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.constants.credits import CREDIT_COLUMNS
from app.services.credits.add_credits import add_credits 


def main() -> None:
    kinds = "|".join(CREDIT_COLUMNS)
    if len(sys.argv) != 4 or sys.argv[2] not in CREDIT_COLUMNS or not sys.argv[3].isdigit():
        sys.exit(f"Usage: grant_credits.py <user-id> <{kinds}> <amount>")
    user_id, kind, amount = sys.argv[1], sys.argv[2], int(sys.argv[3])
    if amount <= 0:
        sys.exit("The amount must be positive.")
    add_credits(user_id, kind, amount, "Granted by the admin", f"admin:{uuid.uuid4()}")
    print(f"Granted {amount} {kind} credits to {user_id}.")


if __name__ == "__main__":
    main()