import re
import unicodedata

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
INLINE_HEADING = re.compile(r"^\s*(?P<keyword>[a-z ]+?)\s*:")
MAX_HEADING_WORDS = 4

SECTION_KEYWORDS = {
    "education": [
        "education",
        "formation",
        "formations",
        "etudes",
        "diplome",
        "diplomes",
        "academic",
        "academique",
    ],
    "experience": [
        "experience",
        "experiences",
        "employment",
        "work history",
        "parcours professionnel",
        "internship",
        "internships",
    ],
    "skills": ["skills", "competences", "competence", "expertise"],
    "profile": ["profile", "profil", "summary", "about me", "objective", "objectif", "a propos"],
}

KEYWORD_TO_SECTION = {
    keyword: section for section, keywords in SECTION_KEYWORDS.items() for keyword in keywords
}

print(KEYWORD_TO_SECTION)


def _strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def _normalize(text: str) -> str:
    """Lowercase, remove accents and punctuation, collapse spaces."""
    return re.sub(r"[\W_]+", " ", _strip_accents(text).lower()).strip()


def find_sections(text: str) -> set[str]:
    """Return which resume sections (education, experience, skills, profile) have a heading."""
    found = set()
    for line in text.splitlines():
        lowered = _strip_accents(line).lower()
        candidates = []

        words = _normalize(lowered).split()
        if 0 < len(words) <= MAX_HEADING_WORDS:
            candidates.append(" ".join(words))

        inline = INLINE_HEADING.match(lowered)
        if inline:
            keyword = _normalize(inline.group("keyword"))
            if 0 < len(keyword.split()) <= 3:
                candidates.append(keyword)

        for candidate in candidates:
            padded = f" {candidate} "
            for keyword, section in KEYWORD_TO_SECTION.items():
                if f" {keyword} " in padded:
                    found.add(section)
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
    parts = [part for part in _normalize(account_name).split() if len(part) >= 2]
    if not parts:
        return False
    required = len(parts) if len(parts) <= 2 else len(parts) - 1
    cv_words = set(_normalize(text).split())
    return sum(part in cv_words for part in parts) >= required


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
