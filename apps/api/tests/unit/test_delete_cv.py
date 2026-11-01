import pytest

import app.services.cv.delete_cv as delete_cv_module
from app.services.cv.delete_cv import delete_cv
from app.types.stored_cv import StoredCV


@pytest.fixture
def calls(monkeypatch):
    recorded = {"rows": [], "files": []}
    monkeypatch.setattr(
        delete_cv_module, "delete_cv_row", lambda row_id: recorded["rows"].append(row_id)
    )
    monkeypatch.setattr(
        delete_cv_module, "delete_cv_file", lambda file_id: recorded["files"].append(file_id)
    )
    return recorded


def test_returns_false_and_deletes_nothing_when_there_is_no_cv(monkeypatch, calls):
    monkeypatch.setattr(delete_cv_module, "get_cv", lambda user_id: None)

    assert delete_cv("user-1") is False
    assert calls == {"rows": [], "files": []}


def test_deletes_the_row_and_the_file(monkeypatch, calls):
    cv = StoredCV(row_id="row-1", file_id="file-1", file_name="cv.pdf", text="x" * 200)
    monkeypatch.setattr(delete_cv_module, "get_cv", lambda user_id: cv)

    assert delete_cv("user-1") is True
    assert calls == {"rows": ["row-1"], "files": ["file-1"]}


def test_deletes_only_the_row_when_there_is_no_file(monkeypatch, calls):
    cv = StoredCV(row_id="row-1", file_id=None, file_name=None, text="x" * 200)
    monkeypatch.setattr(delete_cv_module, "get_cv", lambda user_id: cv)

    assert delete_cv("user-1") is True
    assert calls == {"rows": ["row-1"], "files": []}
