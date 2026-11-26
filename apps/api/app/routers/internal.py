from datetime import UTC, datetime

from fastapi import APIRouter, Depends

from app.dependencies.require_cleanup_token import require_cleanup_token
from app.schemas.cleanup_result import CleanupResult
from app.schemas.maintenance_result import MaintenanceResult
from app.services.cleanup.run_cleanup import run_cleanup
from app.services.subscriptions.run_subscription_maintenance import (
    run_subscription_maintenance,
)

router = APIRouter(prefix="/internal", include_in_schema=False)


@router.post(
    "/cleanup-unactivated-accounts",
    response_model=CleanupResult,
    dependencies=[Depends(require_cleanup_token)],
)
def cleanup_unactivated_accounts(dry_run: bool = False) -> CleanupResult:
    """Delete accounts that missed the setup deadline. A dry run only reports them."""
    return run_cleanup(datetime.now(UTC), dry_run)


@router.post(
    "/subscription-maintenance",
    response_model=MaintenanceResult,
    dependencies=[Depends(require_cleanup_token)],
)
def subscription_maintenance(dry_run: bool = True) -> MaintenanceResult:
    """Explore's monthly reset, the expiry safety net, and renewal reminders. Dry run by default."""
    return run_subscription_maintenance(datetime.now(UTC), dry_run)
