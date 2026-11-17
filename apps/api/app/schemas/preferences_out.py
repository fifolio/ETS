from pydantic import BaseModel, Field


class PreferencesOut(BaseModel):
    theme: str = Field(description="light or dark")
    language: str = Field(description="The language the user chose")
    effective_language: str = Field(
        description="The language to display: the choice, or English until it is translated"
    )
    direction: str = Field(description="ltr or rtl, for the effective language")
    currency: str = Field(description="The currency the user chose")
    currency_symbol: str = Field(description="The symbol for the currency the user chose")
