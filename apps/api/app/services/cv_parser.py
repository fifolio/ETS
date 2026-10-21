import re

import pymupdf

MIN_TEXT_LENGTH = 100
MAX_PAGES = 10


class CVParsingError(Exception):
    """Raised when a CV file can't be turned into usable text."""


def clean_text(text: str) -> str:
    """Normalize whitespace so the model gets compact, readable text."""
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.replace("\x00", "").splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def extract_text_from_pdf(data: bytes) -> str:
    try:
        doc = pymupdf.open(stream=data, filetype="pdf")
    except Exception as exc:
        raise CVParsingError("This file is not a valid PDF") from exc

    with doc:
        if doc.needs_pass:
            raise CVParsingError("This PDF is password protected")
        if doc.page_count > MAX_PAGES:
            raise CVParsingError(f"This PDF has more than {MAX_PAGES} pages")
        text = clean_text("\n".join(page.get_text() for page in doc))

        if len(text) < MIN_TEXT_LENGTH:
            raise CVParsingError("No readable text found. The PDF may be a scanned image.")
        return text
