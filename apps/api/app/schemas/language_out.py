from pydantic import BaseModel, Field


class LanguageOut(BaseModel):
    code: str
    name: str = Field(description="The name in English")
    native_name: str = Field(description="The name in the language itself")
    direction: str = Field(description="ltr or rtl")
    translated: bool = Field(
        description="Whether the web app and the extension have real text for the language. \
            Until it is True, people who pick the language see English."
    )
