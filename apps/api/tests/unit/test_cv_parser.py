import pymupdf
import pytest

from app.services.cv_parser import CVParsingError, clean_text, extract_text_from_pdf

SAMPLE_CV = (
    "Jane Doe\n"
    "Frontend Developer\n"
    "Skills: React, TypeScript, Tailwind CSS\n"
    "Experience: 2 years building web apps\n"
)

def make_pdf(text: str = "") -> bytes:
    doc = pymupdf.open()
    page = doc.new_page()
    if text:
        page.insert_text((72, 72), text)
    data = doc.tobytes()
    doc.close()
    return data

def test_extracts_text_from_pdf():
    text = extract_text_from_pdf(make_pdf(SAMPLE_CV))
    assert "Frontend Developer" in text
    assert "React" in text

def test_clean_text_collapses_whitespace():
    assert clean_text("a   b\t c\n\n\n\n\nd  ") == "a b c\n\nd"

def test_invalid_file_raises():
    with pytest.raises(CVParsingError):
        extract_text_from_pdf(b"this is not a pdf")

def test_blank_pdf_raises():
    with pytest.raises(CVParsingError):
        extract_text_from_pdf(make_pdf())