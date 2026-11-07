from app.services.cleanup.apply_to_each import apply_to_each


def test_runs_the_action_for_every_item():
    seen = []

    assert apply_to_each(["a", "b"], seen.append) == (2, 0)
    assert seen == ["a", "b"]


def test_a_failure_is_counted_and_does_not_stop_the_rest():
    seen = []

    def action(item):
        if item == "b":
            raise ValueError("boom")
        seen.append(item)

    assert apply_to_each(["a", "b", "c"], action) == (2, 1)
    assert seen == ["a", "c"]
