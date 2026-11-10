from app.schemas.site_totals import SiteTotals


def build_site_totals(users: int, scans: int, minutes: float, cash: float) -> SiteTotals:
    return SiteTotals(
        total_users=users,
        total_scans=scans,
        total_minutes_saved=round(minutes, 1),
        total_hours_saved=round(minutes / 60, 1),
        total_cash_saved_usd=round(cash, 2),
    )
