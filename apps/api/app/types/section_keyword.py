from dataclasses import dataclass


@dataclass(frozen=True)
class SectionKeyword:
    text: str  # normalized: lowercase, no accents or punctuation
    section: str
    substring: bool  # True for scripts without spaces between words (Chinese, Japanese, Thai)
