from appwrite.query import Query

from app.services.payments.build_payment_history_queries import build_payment_history_queries


def test_by_default_abandoned_checkouts_are_left_out():
    queries = build_payment_history_queries("user-1", 1, "all", "all")

    assert queries == [
        Query.equal("userId", "user-1"),
        Query.order_desc("$createdAt"),
        Query.limit(10),
        Query.offset(0),
        Query.not_equal("status", "pending"),
    ]


def test_a_later_page_skips_the_earlier_ones():
    assert Query.offset(10) in build_payment_history_queries("user-1", 2, "all", "all")


def test_a_status_filter_matches_that_status_only():
    queries = build_payment_history_queries("user-1", 1, "failed", "all")

    assert Query.equal("status", "failed") in queries
    assert Query.not_equal("status", "pending") not in queries


def test_the_plan_filter_matches_the_paid_plans():
    queries = build_payment_history_queries("user-1", 1, "all", "plan")

    assert Query.equal("sku", ["plan_nextmove", "plan_urgent"]) in queries


def test_the_top_up_filter_matches_top_ups():
    assert Query.equal("sku", "topup") in build_payment_history_queries("user-1", 1, "all", "topup")


def test_filters_combine():
    queries = build_payment_history_queries("user-1", 1, "completed", "topup")

    assert Query.equal("status", "completed") in queries and Query.equal("sku", "topup") in queries
