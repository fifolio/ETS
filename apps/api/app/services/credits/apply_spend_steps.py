from app.services.credits.decrement_balance import decrement_balance
from app.services.credits.increment_balance import increment_balance


def apply_spend_steps(user_id: str, steps: list[tuple[str, int]]) -> bool:
    """Take each step from its column. If one fails, give back the ones already taken."""
    done: list[tuple[str, int]] = []
    for kind, amount in steps:
        if not decrement_balance(user_id, kind, amount):
            for done_kind, done_amount in done:
                increment_balance(user_id, done_kind, done_amount)
            return False
        done.append((kind, amount))
    return True
