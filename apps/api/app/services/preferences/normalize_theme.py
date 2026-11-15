from app.constants.appearance import DEFAULT_THEME, THEMES


def normalize_theme(value: object) -> str:
    return value if isinstance(value, str) and value in THEMES else DEFAULT_THEME
