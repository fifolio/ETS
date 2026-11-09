from types import SimpleNamespace

import app.services.catalog.list_industries as module


def row(row_id, name):
    return SimpleNamespace(id=row_id, data=SimpleNamespace(name=name))


def test_lists_industries_sorted_by_name(monkeypatch):
    rows = [
        row("marketing", "Marketing & Advertising"),
        row("accounting", "Accounting and Finance"),
    ]
    monkeypatch.setattr(module, "iter_table_rows", lambda table_id, model, queries=None: iter(rows))

    result = module.list_industries()

    assert [(item.id, item.name) for item in result] == [
        ("accounting", "Accounting and Finance"),
        ("marketing", "Marketing & Advertising"),
    ]


def test_no_industries_gives_an_empty_list(monkeypatch):
    monkeypatch.setattr(module, "iter_table_rows", lambda table_id, model, queries=None: iter([]))

    assert module.list_industries() == []
