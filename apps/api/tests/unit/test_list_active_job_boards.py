import pytest

import app.services.job_boards.list_active_job_boards as module
from app.types.job_board import JobBoard

BOARD = JobBoard("linkedin", "LinkedIn", "https://www.linkedin.com/jobs", True)


@pytest.fixture
def env(monkeypatch):
    module._cache.update(value=None, expires_at=0.0)
    clock = {"now": 1000.0}
    fetched = []

    def fake_fetch():
        fetched.append(1)
        return [BOARD]

    monkeypatch.setattr(module.time, "monotonic", lambda: clock["now"])
    monkeypatch.setattr(module, "fetch_job_boards", fake_fetch)
    return clock, fetched


def test_the_table_is_read_once_within_the_cache_time(env):
    clock, fetched = env

    module.list_active_job_boards()
    clock["now"] += 59
    module.list_active_job_boards()

    assert len(fetched) == 1


def test_the_table_is_read_again_after_the_cache_time(env):
    clock, fetched = env

    module.list_active_job_boards()
    clock["now"] += 61
    module.list_active_job_boards()

    assert len(fetched) == 2


def test_an_empty_table_is_cached_too(env, monkeypatch):
    clock, fetched = env
    monkeypatch.setattr(module, "fetch_job_boards", lambda: fetched.append(1) or [])

    assert module.list_active_job_boards() == []
    assert module.list_active_job_boards() == []
    assert len(fetched) == 1
