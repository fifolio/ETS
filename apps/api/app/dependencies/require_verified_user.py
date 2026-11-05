from typing import Annotated

from fastapi import Depends, HTTPException

from app.dependencies.get_current_user import get_current_user
from app.types.authenticated_user import AuthenticatedUser


def require_verified_user(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
) -> AuthenticatedUser:
    if not user.email_verified:
        raise HTTPException(status_code=403, detail="Verify your email first.")
    return user
