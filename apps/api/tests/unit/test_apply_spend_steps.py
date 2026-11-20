import app.services.credits.apply_spend_steps as module


def install(monkeypatch, failing_kind=None):
    taken, given_back = [], []

    def decrement(user_id, kind, amount):
        if kind == failing_kind:
            return False
        taken.append((kind, amount))
        return True

    monkeypatch.setattr(module, "decrement_balance", decrement)
    monkeypatch.setattr(
        module, "increment_balance", lambda user_id, kind, amount: given_back.append((kind, amount))
    )
    return taken, given_back


STEPS = [("promotional", 1), ("subscription", 2)]


def test_takes_every_step(monkeypatch):
    taken, given_back = install(monkeypatch)

    assert module.apply_spend_steps("user-1", STEPS) is True
    assert taken == STEPS and given_back == []


def test_a_failing_step_gives_back_the_ones_already_taken(monkeypatch):
    taken, given_back = install(monkeypatch, failing_kind="subscription")

    assert module.apply_spend_steps("user-1", STEPS) is False
    assert given_back == [("promotional", 1)]


def test_nothing_is_given_back_when_the_first_step_fails(monkeypatch):
    _, given_back = install(monkeypatch, failing_kind="promotional")

    assert module.apply_spend_steps("user-1", STEPS) is False
    assert given_back == []
