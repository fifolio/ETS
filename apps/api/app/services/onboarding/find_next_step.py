def find_next_step(steps: dict[str, bool]) -> str | None:
    return next((name for name, done in steps.items() if not done), None)
