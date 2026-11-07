import logging
from collections.abc import Callable, Iterable

logger = logging.getLogger(__name__)


def apply_to_each(items: Iterable[str], action: Callable[[str], None]) -> tuple[int, int]:
    """Run `action` on every item. A failure is logged and counted, and doesn't stop the rest."""
    done = 0
    failed = 0
    for item in items:
        try:
            action(item)
            done += 1
        except Exception:
            logger.exception("Cleanup failed for %s", item)
            failed += 1
    return done, failed
