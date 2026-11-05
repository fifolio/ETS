from typing import Annotated

from fastapi import Depends

from app.dependencies.require_verified_user import require_verified_user
from app.types.authenticated_user import AuthenticatedUser


def require_verified_user_id(
    user: Annotated[AuthenticatedUser, Depends(require_verified_user)],
) -> str:
    return user.id
