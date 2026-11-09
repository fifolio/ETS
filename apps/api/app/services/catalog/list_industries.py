from app.core.config import settings
from app.schemas.industry_row import IndustryRow
from app.schemas.public_industry import PublicIndustry
from app.services.appwrite.iter_table_rows import iter_table_rows


def list_industries() -> list[PublicIndustry]:
    rows = iter_table_rows(settings.appwrite_industries_table_id, IndustryRow)
    industries = [PublicIndustry(id=row.id, name=row.data.name) for row in rows]
    return sorted(industries, key=lambda industry: industry.name.lower())
