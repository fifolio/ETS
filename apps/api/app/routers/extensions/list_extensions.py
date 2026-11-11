from fastapi import APIRouter

from app.routers.extensions.options import EXTENSIONS_ROUTER_OPTIONS
from app.schemas.extension_info import ExtensionInfo
from app.services.extensions.list_user_extensions import list_user_extensions
from app.types.verified_user import VerifiedUserId

router = APIRouter(**EXTENSIONS_ROUTER_OPTIONS)


@router.get("", response_model=list[ExtensionInfo], summary="Your installed extensions")
def list_extensions(user_id: VerifiedUserId) -> list[ExtensionInfo]:
    return list_user_extensions(user_id)
