from appwrite.query import Query

from app.services.credits.build_credit_history_queries import build_credit_history_queries


def test_the_base_query_is_this_users_rows_newest_first_ten_from_the_start():
    queries = build_credit_history_queries("user-1", 1, "all", "all")

    assert queries == [
        Query.equal("userId", "user-1"),
        Query.order_desc("$createdAt"),
        Query.limit(10),
        Query.offset(0),
    ]


def test_a_later_page_skips_the_earlier_ones():
    assert Query.offset(20) in build_credit_history_queries("user-1", 3, "all", "all")


def test_the_type_filter_matches_one_kind():
    assert Query.equal("kind", "purchased") in build_credit_history_queries(
        "user-1", 1, "purchased", "all"
    )


def test_added_means_a_positive_amount():
    assert Query.greater_than("amount", 0) in build_credit_history_queries(
        "user-1", 1, "all", "added"
    )


def test_used_means_a_negative_amount():
    assert Query.less_than("amount", 0) in build_credit_history_queries("user-1", 1, "all", "used")
