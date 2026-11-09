from app.services.feedback.build_metrics import build_metrics
from app.types.usage_stats import UsageStats


def test_the_minutes_saved_come_from_the_stored_total():
    metrics = build_metrics(UsageStats(scans=3, words=1800, minutes=8.0, cash=6.6667))

    assert (metrics.scans, metrics.words, metrics.minutes_saved) == (3, 1800, 8.0)


def test_the_minutes_are_rounded_to_one_decimal():
    assert build_metrics(UsageStats(scans=1, words=100, minutes=0.4444)).minutes_saved == 0.4


def test_no_usage_means_zero_everything():
    metrics = build_metrics(UsageStats(scans=0, words=0))

    assert (metrics.scans, metrics.words, metrics.minutes_saved) == (0, 0, 0.0)


def test_totals_far_beyond_any_limit_still_add_up():
    metrics = build_metrics(UsageStats(scans=10_000, words=7_000_000, minutes=31111.1111))

    assert (metrics.scans, metrics.minutes_saved) == (10_000, 31111.1)
