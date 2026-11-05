from typing import Annotated

from fastapi import Depends

from app.dependencies.require_verified_user import require_verified_user
from app.dependencies.require_verified_user_id import require_verified_user_id
from app.types.authenticated_user import AuthenticatedUser

VerifiedUser = Annotated[AuthenticatedUser, Depends(require_verified_user)]
VerifiedUserId = Annotated[str, Depends(require_verified_user_id)]
