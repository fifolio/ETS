from typing import Annotated

from fastapi import Depends

from app.dependencies.get_current_user import get_current_user
from app.dependencies.get_current_user_id import get_current_user_id
from app.types.authenticated_user import AuthenticatedUser

CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]
CurrentUserId = Annotated[str, Depends(get_current_user_id)]
