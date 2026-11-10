import pytest

import app.services.stats.get_site_totals as module
from app.services.stats.build_site_totals import build_site_totals


@pytest.fixture
def env(monkeypatch):
    module._cache.update(value=None, expires_at=0.0)
    clock = {"now": 1000.0}
    computed = []

    def compute():
        computed.append(1)
        return build_site_totals(len(computed), 0, 0.0, 0.0)

    monkeypatch.setattr(module.time, "monotonic", lambda: clock["now"])
    monkeypatch.setattr(module, "compute_site_totals", compute)
    return clock, computed


def test_the_totals_are_computed_once_within_the_cache_time(env):
    clock, computed = env

    first = module.get_site_totals()
    clock["now"] += 86400 - 1
    second = module.get_site_totals()

    assert first == second
    assert len(computed) == 1


def test_the_totals_are_recomputed_after_the_cache_time(env):
    clock, computed = env

    module.get_site_totals()
    clock["now"] += 86400 + 1
    module.get_site_totals()

    assert len(computed) == 2
