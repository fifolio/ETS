import app.services.extensions.touch_extension as module


def install(monkeypatch, row_id):
    updated, incremented = [], []
    monkeypatch.setattr(module, "find_extension_id", lambda user_id, install_id: row_id)
    monkeypatch.setattr(module, "update_extension", lambda rid, data: updated.append((rid, data)))
    monkeypatch.setattr(module, "increment_extension_scans", incremented.append)
    return updated, incremented


def test_a_counted_use_updates_the_time_and_adds_a_scan(monkeypatch):
    updated, incremented = install(monkeypatch, "row-1")

    module.touch_extension("user-1", "install-12345678", counted=True)

    assert updated[0][0] == "row-1" and "lastUsedAt" in updated[0][1]
    assert incremented == ["row-1"]


def test_an_uncounted_use_only_updates_the_time(monkeypatch):
    updated, incremented = install(monkeypatch, "row-1")

    module.touch_extension("user-1", "install-12345678", counted=False)

    assert len(updated) == 1
    assert incremented == []


def test_an_install_that_never_registered_is_ignored(monkeypatch):
    updated, incremented = install(monkeypatch, None)

    module.touch_extension("user-1", "install-12345678", counted=True)

    assert updated == [] and incremented == []
