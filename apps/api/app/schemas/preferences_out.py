from pydantic import BaseModel, Field


class PreferencesOut(BaseModel):
    theme: str = Field(description="light or dark")
    language: str = Field(description="The language the user chose")
    effective_language: str = Field(
        description="The language to display: the choice, or English until it is translated"
    )
    direction: str = Field(description="ltr or rtl, for the effective language")
