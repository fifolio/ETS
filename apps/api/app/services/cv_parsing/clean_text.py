import re


def clean_text(text: str) -> str:
    """Normalize whitespace so the model gets compact, readable text."""
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.replace("\x00", "").splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
