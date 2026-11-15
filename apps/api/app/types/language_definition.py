from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageDefinition:
    code: str
    name: str
    native_name: str
    direction: str  # "ltr" or "rtl"
    translated: bool
