from app.constants.cv_validation import INLINE_HEADING, MAX_HEADING_WORDS
from app.services.text.normalize import normalize
from app.services.text.strip_accents import strip_accents


def heading_candidates(line: str) -> list[str]:
    """Return the parts of a line that could be a section heading."""
    lowered = strip_accents(line).lower()
    candidates = []

    normalized = normalize(lowered)
    if 0 < len(normalized.split()) <= MAX_HEADING_WORDS:
        candidates.append(normalized)

    inline = INLINE_HEADING.match(lowered)  # for lines like "Skills: React, Docker"
    if inline:
        keyword = normalize(inline.group("keyword"))
        if 0 < len(keyword.split()) <= 3:
            candidates.append(keyword)

    return candidates
