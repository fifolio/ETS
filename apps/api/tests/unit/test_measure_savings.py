import app.services.usage.measure_savings as module
from app.types.authenticated_user import AuthenticatedUser


def make_user(prefs):
    return AuthenticatedUser("user-1", "Jane Doe", "jane.doe@example.com", True, prefs)


def test_the_cash_uses_the_rate_of_the_job_from_the_table(monkeypatch):
    monkeypatch.setattr(module, "get_job_rate", lambda job_id: 50.0)

    savings = module.measure_savings(make_user({"jobId": "job-1"}), 1125)

    assert (savings.minutes, savings.cash) == (5.0, 4.1667)


def test_a_rate_edited_in_the_users_own_preferences_is_ignored(monkeypatch):
    monkeypatch.setattr(module, "get_job_rate", lambda job_id: 50.0)

    savings = module.measure_savings(make_user({"jobId": "job-1", "hourlyRateUsd": 9999}), 1125)

    assert savings.cash == 4.1667


def test_no_job_in_the_preferences_means_no_cash(monkeypatch):
    monkeypatch.setattr(module, "get_job_rate", lambda job_id: pytest_fail())

    savings = module.measure_savings(make_user({}), 1125)

    assert (savings.minutes, savings.cash) == (5.0, 0.0)


def test_a_job_that_no_longer_exists_means_no_cash(monkeypatch):
    monkeypatch.setattr(module, "get_job_rate", lambda job_id: None)

    savings = module.measure_savings(make_user({"jobId": "deleted"}), 1125)

    assert (savings.minutes, savings.cash) == (5.0, 0.0)


def test_a_failed_rate_lookup_still_counts_the_minutes(monkeypatch):
    def fail(job_id):
        raise RuntimeError("table down")

    monkeypatch.setattr(module, "get_job_rate", fail)

    savings = module.measure_savings(make_user({"jobId": "job-1"}), 1125)

    assert (savings.minutes, savings.cash) == (5.0, 0.0)


def pytest_fail():
    raise AssertionError("the rate must not be looked up without a job")
