from app.services.stats.build_site_totals import build_site_totals


def test_rounds_each_total_sensibly():
    totals = build_site_totals(users=3, scans=120, minutes=125.04, cash=98.7654)

    assert totals.model_dump() == {
        "total_users": 3,
        "total_scans": 120,
        "total_minutes_saved": 125.0,
        "total_hours_saved": 2.1,
        "total_cash_saved_usd": 98.77,
    }


def test_hours_are_the_minutes_divided_by_60():
    assert build_site_totals(1, 1, 90.0, 0.0).total_hours_saved == 1.5


def test_an_empty_table_gives_zeros():
    totals = build_site_totals(0, 0, 0.0, 0.0)

    assert (totals.total_users, totals.total_scans, totals.total_cash_saved_usd) == (0, 0, 0.0)
