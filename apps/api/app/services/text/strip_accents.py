import unicodedata


def strip_accents(text: str) -> str:
    """Remove accents and other combining marks (é becomes e, Arabic vowel marks vanish, ...)."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(char for char in decomposed if not unicodedata.combining(char))
