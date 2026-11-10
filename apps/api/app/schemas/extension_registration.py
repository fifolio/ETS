from pydantic import BaseModel, Field


class ExtensionRegistration(BaseModel):
    install_id: str = Field(
        pattern=r"^[A-Za-z0-9-]{8,64}$",
        description="Random ID the extension creates once per browser install",
    )
    browser: str = Field(max_length=50, description="For example Chrome or Edge")
    browser_version: str = Field(default="", max_length=50)
    os: str = Field(default="", max_length=50)
    extension_version: str = Field(default="", max_length=20)
