from functools import lru_cache

from app.constants import cv_sections as section_constants
from app.services.cv_sections.read_language_file import read_language_file
from app.services.text.has_unspaced_script import has_unspaced_script
from app.services.text.normalize import normalize
from app.types.section_keyword import SectionKeyword


@lru_cache
def load_keywords() -> tuple[SectionKeyword, ...]:
    """Load the heading keywords from every language file in the cv_sections folder."""
    owners: dict[str, str] = {}
    keywords = []
    for path in sorted(section_constants.SECTIONS_DIR.glob("*.json")):
        data = read_language_file(path)
        for section in section_constants.SECTION_NAMES:
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
