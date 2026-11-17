from types import SimpleNamespace

import app.services.currencies.list_currencies as module


def row(code, name, symbol, rate):
    return SimpleNamespace(
        id=code, data=SimpleNamespace(name=name, symbol=symbol, rateFromUsd=rate)
    )


def test_lists_currencies_sorted_by_code(monkeypatch):
    module._cache.update(value=None, expires_at=0.0)
    monkeypatch.setattr(
        module,
        "iter_table_rows",
        lambda table_id, model: iter(
            [
                row("usd", "US Dollar", "$", 1.0),
                row("eur", "Euro", "€", 0.92),
            ]
        ),
    )

    result = module.list_currencies()

    assert [c.code for c in result] == ["eur", "usd"]
    assert result[0].rate_from_usd == 0.92
