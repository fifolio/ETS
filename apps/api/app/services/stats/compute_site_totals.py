from app.core.config import settings
from app.schemas.site_totals import SiteTotals
from app.schemas.usage_row import UsageRow
from app.services.appwrite.iter_table_rows import iter_table_rows
from app.services.stats.build_site_totals import build_site_totals


def compute_site_totals() -> SiteTotals:
    """Add up the whole usage_stats table, one page at a time."""
    users = scans = 0
    minutes = cash = 0.0
    for row in iter_table_rows(settings.appwrite_usage_table_id, UsageRow):
        users += 1
        scans += row.data.scanCount
        minutes += row.data.minutesTotal
        cash += row.data.cashTotal
    return build_site_totals(users, scans, minutes, cash)
