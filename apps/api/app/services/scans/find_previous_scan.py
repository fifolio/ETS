import logging

from app.schemas.match_result import MatchResult
from app.services.scans.find_scan_result import find_scan_result
from app.services.scans.hash_job_url import hash_job_url

logger = logging.getLogger(__name__)


def find_previous_scan(user_id: str, job_url: str | None) -> MatchResult | None:
    """The stored result of a page this user already scanned, or None. Never raises."""
    if not job_url:
        return None
    try:
        return find_scan_result(user_id, hash_job_url(job_url))
    except Exception:
        logger.exception("Could not check for a previous scan")
        return None
