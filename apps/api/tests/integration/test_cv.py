import pymupdf
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.types.stored_cv import StoredCV

pytestmark = pytest.mark.usefixtures("logged_in")

client = TestClient(app)

# Matches the test user in conftest.py: Jane Doe, jane.doe@example.com
SAMPLE_CV = (
    "Jane Doe\n"
    "jane.doe@example.com\n"
    "Frontend Developer\n"
    "Skills: React, TypeScript, Tailwind CSS\n"
    "Experience: 2 years building web apps\n"
)


def make_pdf(text: str) -> bytes:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    data = doc.tobytes()
    doc.close()
    return data


def test_get_cv_returns_404_when_missing(monkeypatch):
    monkeypatch.setattr("app.routers.cv.read_cv.get_cv", lambda user_id: None)
    assert client.get("/cv").status_code == 404


def test_get_cv_returns_info(monkeypatch):
    stored = StoredCV("row-1", "file-1", "cv.pdf", "x" * 500)
    monkeypatch.setattr("app.routers.cv.read_cv.get_cv", lambda user_id: stored)

    response = client.get("/cv")

    assert response.status_code == 200
    assert response.json() == {"file_name": "cv.pdf", "characters": 500}


def test_upload_cv_parses_validates_and_saves(monkeypatch):
    saved = {}

    def fake_save(user_id, file_name, pdf_bytes, text):
        saved.update(user_id=user_id, file_name=file_name, text=text)

    monkeypatch.setattr("app.routers.cv.upload_cv.save_cv", fake_save)

    response = client.post(
        "/cv", files={"file": ("my-cv.pdf", make_pdf(SAMPLE_CV), "application/pdf")}
    )

    assert response.status_code == 201
    assert saved["user_id"] == "user-1"
    assert saved["file_name"] == "my-cv.pdf"
    assert "Frontend Developer" in saved["text"]


def test_upload_rejects_non_pdf():
    response = client.post("/cv", files={"file": ("cv.pdf", b"not a pdf", "application/pdf")})

    assert response.status_code == 422
    assert response.json()["problems"]


def test_upload_rejects_cv_that_does_not_match_the_account(monkeypatch):
    monkeypatch.setattr(
        "app.routers.cv.upload_cv.save_cv", lambda *args: pytest.fail("must not save")
    )
    other_cv = SAMPLE_CV.replace("Jane Doe", "John Smith").replace(
        "jane.doe@example.com", "john@other.com"
    )

    response = client.post("/cv", files={"file": ("cv.pdf", make_pdf(other_cv), "application/pdf")})

    assert response.status_code == 422
    body = response.json()
    assert body["detail"] == "The CV did not pass validation."
    assert len(body["problems"]) == 2  # wrong email and wrong name


def test_upload_rejects_large_file():
    big = b"0" * (5 * 1024 * 1024 + 1)
    response = client.post("/cv", files={"file": ("cv.pdf", big, "application/pdf")})
    assert response.status_code == 413
