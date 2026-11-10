import logging

from appwrite.exception import AppwriteException

from app.schemas.match_result import MatchResult
from app.services.extensions.record_extension_use import record_extension_use
from app.services.scans.hash_job_url import hash_job_url
from app.services.scans.save_scan import save_scan
from app.services.text.count_words import count_words
from app.services.usage.measure_savings import measure_savings
from app.services.usage.record_scan_usage import record_scan_usage
from app.types.authenticated_user import AuthenticatedUser

logger = logging.getLogger(__name__)


def record_scan(
    user: AuthenticatedUser,
    result: MatchResult,
    job_url: str | None,
    job_title: str | None,
    job_text: str,
    install_id: str | None = None,
) -> None:
    """Save the scan and add it to the user's totals. Never raises: the verdict matters more."""
    words = count_words(job_text)
    savings = measure_savings(user, words)
    url_hash = hash_job_url(job_url) if job_url else None

    try:
        save_scan(user.id, result, job_url, job_title, words, savings, url_hash)
    except AppwriteException as exc:
        if exc.code == 409:
            # The same page was scanned at the same moment: the first request already counted.
            logger.info("This page was already recorded for the user")
            return
        logger.exception("Could not save scan history")
    except Exception:
        logger.exception("Could not save scan history")

    try:
        record_scan_usage(user.id, words, savings)
    except Exception:
        logger.exception("Could not record usage")

    record_extension_use(user.id, install_id, counted=True)
