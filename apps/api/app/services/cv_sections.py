import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.services.text_utils import has_unspaced_script, normalize

SECTIONS_DIR = Path(__file__).resolve().parent.parent / "resources" / "cv_sections"
SECTION_NAMES = ("education", "experience", "skills", "profile")


@dataclass(frozen=True)
class SectionKeyword:
    text: str  # normalized: lowercase, no accents or punctuation
    section: str
    substring: bool  # True for scripts without spaces between words (Chinese, Japanese, Thai)


@lru_cache
def load_keywords() -> tuple[SectionKeyword, ...]:
    """Load the heading keywords from every language file in the cv_sections folder."""
    owners: dict[str, str] = {}
    keywords = []
    for path in sorted(SECTIONS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for section in SECTION_NAMES:
            for raw in data.get(section, []):
                text = normalize(raw)
                if not text:
                    continue
                if text in owners:
                    if owners[text] != section:
                        raise ValueError(
                            f"{path.name}: '{raw}' is listed under both "
                            f"'{owners[text]}' and '{section}'"
                        )
                    continue
                owners[text] = section
                keywords.append(SectionKeyword(text, section, has_unspaced_script(text)))
    return tuple(keywords)
