import app.services.cv.save_cv as module
from app.types.stored_cv import StoredCV


def install(monkeypatch, existing):
    created, updated = [], []
    monkeypatch.setattr(module, "get_cv", lambda user_id: existing)
    monkeypatch.setattr(module, "create_cv_row", created.append)
    monkeypatch.setattr(
        module, "update_cv_row", lambda row_id, data: updated.append((row_id, data))
    )
    return created, updated


def test_creates_a_row_for_a_first_cv(monkeypatch):
    created, updated = install(monkeypatch, None)

    module.save_cv("user-1", "cv.pdf", "my cv text")

    assert created == [{"userId": "user-1", "fileName": "cv.pdf", "text": "my cv text"}]
    assert updated == []


def test_replaces_the_text_of_an_existing_cv(monkeypatch):
    existing = StoredCV(row_id="row-1", file_name="old.pdf", text="old text")
    created, updated = install(monkeypatch, existing)

    module.save_cv("user-1", "new.pdf", "new text")

    assert created == []
    assert updated == [("row-1", {"userId": "user-1", "fileName": "new.pdf", "text": "new text"})]


def test_stores_only_the_user_the_file_name_and_the_text(monkeypatch):
    created, _ = install(monkeypatch, None)

    module.save_cv("user-1", "cv.pdf", "text")

    assert set(created[0]) == {"userId", "fileName", "text"}
