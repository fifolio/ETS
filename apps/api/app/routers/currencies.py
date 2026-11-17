from fastapi import APIRouter, Response

from app.schemas.currency_out import CurrencyOut
from app.services.currencies.list_currencies import list_currencies

router = APIRouter(tags=["currencies"], prefix="/currencies")


@router.get("", response_model=list[CurrencyOut], summary="Currencies for display")
def currencies(response: Response) -> list[CurrencyOut]:
    response.headers["Cache-Control"] = "public, max-age=300"
    return list_currencies()
