from app.services.cv_sections.load_keywords import load_keywords
from app.services.cv_validation.heading_candidates import heading_candidates
from app.services.cv_validation.keyword_matches import keyword_matches


def find_sections(text: str) -> set[str]:
    """Return which resume sections (education, experience, skills, profile) have a heading."""
    keywords = load_keywords()
    found: set[str] = set()
    for line in text.splitlines():
        for candidate in heading_candidates(line):
            for keyword in keywords:
                if keyword.section not in found and keyword_matches(candidate, keyword):
                    found.add(keyword.section)
    return found
