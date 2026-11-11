import pytest
from appwrite.exception import AppwriteException

import app.services.extensions.register_extension as module
from app.schemas.extension_registration import ExtensionRegistration

REGISTRATION = ExtensionRegistration(
    install_id="install-12345678",
    browser="Chrome",
    browser_version="130.0",
    os="Windows",
    extension_version="0.1.0",
)


def install(monkeypatch, finds, create_error=None):
    created, updated = [], []
    results = list(finds)
    monkeypatch.setattr(module, "find_extension_id", lambda user_id, install_id: results.pop(0))

    def create(data):
        if create_error:
            raise create_error
        created.append(data)

    monkeypatch.setattr(module, "create_extension", create)
    monkeypatch.setattr(
        module, "update_extension", lambda row_id, data: updated.append((row_id, data))
    )
    return created, updated


def test_a_new_install_is_created_with_zero_scans(monkeypatch):
    created, updated = install(monkeypatch, [None])

    assert module.register_extension("user-1", REGISTRATION) is True
    assert created[0]["userId"] == "user-1"
    assert created[0]["installId"] == "install-12345678"
    assert created[0]["scanCount"] == 0
    assert updated == []
    assert "installedAt" in created[0]


def test_a_known_install_is_refreshed_without_touching_its_scan_count(monkeypatch):
    created, updated = install(monkeypatch, ["row-1"])

    assert module.register_extension("user-1", REGISTRATION) is False
    assert created == []
    assert updated[0][0] == "row-1"
    assert "scanCount" not in updated[0][1]
    assert updated[0][1]["browser"] == "Chrome"
    assert "installedAt" not in updated[0][1]


def test_a_simultaneous_registration_falls_back_to_refreshing_that_row(monkeypatch):
    created, updated = install(
        monkeypatch, [None, "row-1"], create_error=AppwriteException("exists", 409)
    )

    assert module.register_extension("user-1", REGISTRATION) is False
    assert updated[0][0] == "row-1"


def test_other_errors_are_raised(monkeypatch):
    install(monkeypatch, [None], create_error=AppwriteException("boom", 500))

    with pytest.raises(AppwriteException):
        module.register_extension("user-1", REGISTRATION)
