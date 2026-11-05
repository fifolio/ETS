from app.services.profile.is_filled_text import is_filled_text


def is_filled_list(value: object, allowed: tuple[str, ...] | None = None) -> bool:
    """True for a non-empty list of non-blank strings, all from `allowed` when it is given."""
    if not isinstance(value, list) or not value:
        return False
    if not all(is_filled_text(item) for item in value):
        return False
    return allowed is None or all(item in allowed for item in value)
