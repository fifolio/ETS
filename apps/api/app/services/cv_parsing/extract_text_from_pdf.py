import pymupdf

from app.constants.cv_parsing import MAX_PAGES, MIN_TEXT_LENGTH
from app.exceptions.cv_parsing_error import CVParsingError
from app.services.cv_parsing.clean_text import clean_text


def extract_text_from_pdf(data: bytes) -> str:
    try:
        doc = pymupdf.open(stream=data, filetype="pdf")
    except Exception as exc:
        raise CVParsingError("This file is not a valid PDF.") from exc

    with doc:
        if doc.needs_pass:
            raise CVParsingError("This PDF is password protected.")
        if doc.page_count > MAX_PAGES:
            raise CVParsingError(f"This PDF has more than {MAX_PAGES} pages.")
        text = clean_text("\n".join(page.get_text() for page in doc))

    if len(text) < MIN_TEXT_LENGTH:
        raise CVParsingError("No readable text found. The PDF may be a scanned image.")
    return text
