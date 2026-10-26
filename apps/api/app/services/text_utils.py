import re
import unicodedata

# Scripts written without spaces between words: Thai, Japanese kana, and Chinese ideographs.
UNSPACED_SCRIPTS = re.compile(r"[\u0e00-\u0e7f\u3040-\u30ff\u3400-\u9fff]")


def strip_accents(text: str) -> str:
    """Remove accents and other combining marks (é becomes e, Arabic vowel marks vanish, ...)."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def normalize(text: str) -> str:
    """Lowercase, remove accents and punctuation, and collapse spaces."""
    return re.sub(r"[\W_]+", " ", strip_accents(text).lower()).strip()


def has_unspaced_script(text: str) -> bool:
    return bool(UNSPACED_SCRIPTS.search(text))
