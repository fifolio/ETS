from datetime import UTC, datetime

from fastapi import APIRouter, Depends

from app.dependencies.require_cleanup_token import require_cleanup_token
from app.schemas.cleanup_result import CleanupResult
from app.services.cleanup.run_cleanup import run_cleanup

router = APIRouter(prefix="/internal", include_in_schema=False)


@router.post(
    "/cleanup-unactivated-accounts",
    response_model=CleanupResult,
    dependencies=[Depends(require_cleanup_token)],
)
def cleanup_unactivated_accounts(dry_run: bool = False) -> CleanupResult:
    """Delete accounts that missed the setup deadline. A dry run only reports them."""
    return run_cleanup(datetime.now(UTC), dry_run)
