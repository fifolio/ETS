from fastapi import APIRouter, Response

from app.schemas.language_out import LanguageOut
from app.services.preferences.list_languages import list_languages

router = APIRouter(tags=["preferences"])


@router.get(
    "/languages",
    response_model=list[LanguageOut],
    summary="The languages ETS offers",
    description="Public. Languages that aren't translated yet fall back to English.",
)
def languages(response: Response) -> list[LanguageOut]:
    response.headers["Cache-Control"] = "public, max-age=300"
    return list_languages()
