from typing import Annotated

from fastapi import Depends

from app.dependencies.get_current_user import get_current_user
from app.types.authenticated_user import AuthenticatedUser


def get_current_user_id(user: Annotated[AuthenticatedUser, Depends(get_current_user)]) -> str:
    return user.id
