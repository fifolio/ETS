from app.services.cleanup.find_orphan_user_ids import find_orphan_user_ids


def test_returns_data_owners_that_have_no_account():
    assert find_orphan_user_ids({"a", "b"}, {"b", "d", "c"}) == ["c", "d"]


def test_returns_nothing_when_every_owner_still_exists():
    assert find_orphan_user_ids({"a", "b"}, {"a"}) == []
