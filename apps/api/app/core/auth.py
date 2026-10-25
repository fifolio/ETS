from typing import Annotated

from appwrite.exception import AppwriteException
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.services.appwrite_client import AuthenticatedUser, verify_jwt

bearer_scheme = HTTPBearer(auto_error=False, description="Appwrite JWT of the logged-in user")


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> AuthenticatedUser:
    unauthorized = HTTPException(
        status_code=401,
        detail="Invalid or missing token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    try:
        return verify_jwt(credentials.credentials)
    except AppwriteException as exc:
        if exc.code == 401:
            raise unauthorized from exc
        raise  # Appwrite itself is failing, so the 502 handler deal with it


CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]


def get_current_user_id(user: CurrentUser) -> str:
    return user.id


CurrentUserId = Annotated[str, Depends(get_current_user_id)]
