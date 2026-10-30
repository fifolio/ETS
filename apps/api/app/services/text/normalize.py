import re

from app.services.text.strip_accents import strip_accents


def normalize(text: str) -> str:
    """Lowercase, remove accents and punctuation, and collapse spaces."""
    return re.sub(r"[\W_]+", " ", strip_accents(text).lower()).strip()
