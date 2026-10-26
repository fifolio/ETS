import re

from app.services.cv_sections import SectionKeyword, load_keywords
from app.services.text_utils import has_unspaced_script, normalize, strip_accents

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
INLINE_HEADING = re.compile(r"^\s*(?P<keyword>[^:：]{1,40}?)\s*[:：]")
MAX_HEADING_WORDS = 4
MAX_UNSPACED_LINE_CHARS = 30  # Chinese, Japanese, Thai have no spaces, so limit by length
UNSPACED_HEADING_WINDOW = 12  # for those scripts, the keyword must start near the line start


def _heading_candidates(line: str) -> list[str]:
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


def _matches(candidate: str, keyword: SectionKeyword) -> bool:
    if keyword.substring:
        return (
            len(candidate) <= MAX_UNSPACED_LINE_CHARS
            and keyword.text in candidate[:UNSPACED_HEADING_WINDOW]
        )
    return f" {keyword.text} " in f" {candidate} "


def find_sections(text: str) -> set[str]:
    """Return which resume sections (education, experience, skills, profile) have a heading."""
    keywords = load_keywords()
    found: set[str] = set()
    for line in text.splitlines():
        for candidate in _heading_candidates(line):
            for keyword in keywords:
                if keyword.section not in found and _matches(candidate, keyword):
                    found.add(keyword.section)
    return found


def _email_problem(text: str, account_email: str) -> str | None:
    if account_email.lower() in text.lower():
        return None
    if not EMAIL_PATTERN.search(text):
        return "No email address found on the CV. Add the email you signed up with."
    return (
        "The CV doesn't contain your account email address. "
        "Add it to your CV, or sign up with the email shown on it."
    )


def _name_matches(text: str, account_name: str) -> bool:
    parts = [part for part in normalize(account_name).split() if len(part) >= 2]
    if not parts:
        return False
    required = len(parts) if len(parts) <= 2 else len(parts) - 1
    normalized_cv = normalize(text)
    cv_words = set(normalized_cv.split())

    def appears(part: str) -> bool:
        if has_unspaced_script(part):
            return part in normalized_cv  # Chinese, Japanese, Thai names have no spaces around
        return part in cv_words

    return sum(appears(part) for part in parts) >= required


def validate_cv(text: str, *, account_name: str, account_email: str) -> list[str]:
    """Return a list of problems with the CV. An empty list means it's accepted."""
    problems = []

    email_problem = _email_problem(text, account_email)
    if email_problem:
        problems.append(email_problem)

    if not _name_matches(text, account_name):
        problems.append(
            "The CV doesn't contain your account name. "
            "Make sure the name on your CV matches the name you signed up with."
        )

    if not find_sections(text):
        problems.append(
            "No Education, Experience, Skills, or Profile section found. "
            "Make sure at least one of these headings appears in your CV."
        )

    return problems
