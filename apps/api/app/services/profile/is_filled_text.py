def is_filled_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())
