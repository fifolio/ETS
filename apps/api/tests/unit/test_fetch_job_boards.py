from types import SimpleNamespace

import app.services.job_boards.fetch_job_boards as module


def row(row_id, name, url, tier="explore", active=True):
    data = SimpleNamespace(name=name, url=url, minPlan=tier, isActive=active)
    return SimpleNamespace(id=row_id, data=data)


def install(monkeypatch, rows):
    monkeypatch.setattr(module, "iter_table_rows", lambda table_id, model: iter(rows))


def test_maps_the_rows_to_job_boards(monkeypatch):
    install(monkeypatch, [row("indeed", "Indeed", "https://www.indeed.com", "nextmove")])

    board = module.fetch_job_boards()[0]

    assert (board.id, board.name, board.url, board.min_plan) == (
        "indeed",
        "Indeed",
        "https://www.indeed.com",
        "nextmove",
    )


def test_hidden_boards_are_left_out(monkeypatch):
    install(
        monkeypatch,
        [row("a", "A", "https://a.example"), row("b", "B", "https://b.example", active=False)],
    )

    assert [board.id for board in module.fetch_job_boards()] == ["a"]


def test_boards_are_sorted_by_name(monkeypatch):
    install(
        monkeypatch, [row("z", "zip", "https://z.example"), row("a", "Alpha", "https://a.example")]
    )

    assert [board.id for board in module.fetch_job_boards()] == ["a", "z"]


def test_a_board_without_a_known_tier_becomes_urgent_only(monkeypatch):
    install(
        monkeypatch,
        [
            row("x", "X", "https://x.example", tier=None),
            row("y", "Y", "https://y.example", tier="gold"),
        ],
    )

    assert [board.min_plan for board in module.fetch_job_boards()] == ["urgent", "urgent"]
