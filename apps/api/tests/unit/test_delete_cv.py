import app.services.cv.delete_cv as module
from app.types.stored_cv import StoredCV


def test_returns_false_and_deletes_nothing_when_there_is_no_cv(monkeypatch):
    deleted = []
    monkeypatch.setattr(module, "get_cv", lambda user_id: None)
    monkeypatch.setattr(module, "delete_cv_row", deleted.append)

    assert module.delete_cv("user-1") is False
    assert deleted == []


def test_deletes_the_row(monkeypatch):
    deleted = []
    cv = StoredCV(row_id="row-1", file_name="cv.pdf", text="x" * 200)
    monkeypatch.setattr(module, "get_cv", lambda user_id: cv)
    monkeypatch.setattr(module, "delete_cv_row", deleted.append)

    assert module.delete_cv("user-1") is True
    assert deleted == ["row-1"]
