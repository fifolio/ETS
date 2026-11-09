import logging

from app.services.catalog.get_job_rate import get_job_rate
from app.services.usage.minutes_to_cash import minutes_to_cash
from app.services.usage.words_to_minutes import words_to_minutes
from app.types.authenticated_user import AuthenticatedUser
from app.types.scan_savings import ScanSavings

logger = logging.getLogger(__name__)


def measure_savings(user: AuthenticatedUser, words: int) -> ScanSavings:
    """Minutes and cash a scan of `words` words saved.

    The rate comes from the jobs table, never from the user's own (editable) preferences.
    """
    minutes = words_to_minutes(words)
    job_id = user.prefs.get("jobId")
    rate = None
    if isinstance(job_id, str) and job_id:
        try:
            rate = get_job_rate(job_id)
        except Exception:
            logger.exception("Could not read the hourly rate of job %s", job_id)
    if rate is None:
        logger.warning("No hourly rate for user %s, so the cash saved is 0", user.id)
        return ScanSavings(minutes=minutes, cash=0.0)
    return ScanSavings(minutes=minutes, cash=minutes_to_cash(minutes, rate))
