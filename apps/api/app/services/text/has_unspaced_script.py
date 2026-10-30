from app.constants.text import UNSPACED_SCRIPTS


def has_unspaced_script(text: str) -> bool:
    return bool(UNSPACED_SCRIPTS.search(text))
