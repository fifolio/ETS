from datetime import UTC, datetime

from app.constants.credits import CREDITS_PER_SCAN
from app.schemas.credits_out import CreditsOut
from app.services.credits.ensure_credit_account import ensure_credit_account
from app.services.credits.read_credit_balance import get_credit_balance
from app.types.credit_balance import CreditBalance


def read_user_credits(user_id: str) -> CreditsOut:
    ensure_credit_account(user_id, datetime.now(UTC))
    balance = get_credit_balance(user_id) or CreditBalance(0, 0, 0)
    return CreditsOut(
        subscription=balance.subscription,
        promotional=balance.promotional,
        purchased=balance.purchased,
        total=balance.total,
        credits_per_scan=CREDITS_PER_SCAN,
    )
