from types import SimpleNamespace

import app.services.extensions.list_user_extensions as module


def row(row_id, last_used, scans=0):
    data = SimpleNamespace(
        browser="Chrome",
        browserVersion="130",
        os="Windows",
        extensionVersion="0.1.0",
        installedAt="2026-11-01T10:00:00+00:00",
        lastUsedAt=last_used,
        scanCount=scans,
    )
    return SimpleNamespace(id=row_id, data=data)


def install(monkeypatch, rows):
    seen = {}

    def fake_iter(table_id, model, queries=None):
        seen["queries"] = queries
        return iter(rows)

    monkeypatch.setattr(module, "iter_table_rows", fake_iter)
    return seen


def test_lists_the_most_recently_used_install_first(monkeypatch):
    install(
        monkeypatch,
        [row("old", "2026-11-02T10:00:00+00:00"), row("new", "2026-11-09T10:00:00+00:00")],
    )

    assert [item.id for item in module.list_user_extensions("user-1")] == ["new", "old"]


def test_an_install_that_was_never_used_comes_last(monkeypatch):
    install(monkeypatch, [row("never", None), row("used", "2026-11-02T10:00:00+00:00")])

    assert [item.id for item in module.list_user_extensions("user-1")] == ["used", "never"]


def test_asks_only_for_the_installs_of_this_user(monkeypatch):
    seen = install(monkeypatch, [row("a", None, scans=3)])

    items = module.list_user_extensions("user-1")

    assert "userId" in seen["queries"][0] and "user-1" in seen["queries"][0]
    assert (items[0].browser, items[0].scan_count) == ("Chrome", 3)
