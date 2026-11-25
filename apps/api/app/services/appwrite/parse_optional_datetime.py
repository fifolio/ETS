from datetime import datetime

from app.services.appwrite.parse_appwrite_datetime import parse_appwrite_datetime


def parse_optional_datetime(text: object) -> datetime | None:
    if not isinstance(text, str) or not text:
        return None
    try:
        return parse_appwrite_datetime(text)
    except ValueError:
        return None
