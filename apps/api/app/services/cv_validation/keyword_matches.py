from app.constants.cv_validation import MAX_UNSPACED_LINE_CHARS, UNSPACED_HEADING_WINDOW
from app.types.section_keyword import SectionKeyword


def keyword_matches(candidate: str, keyword: SectionKeyword) -> bool:
    if keyword.substring:
        return (
            len(candidate) <= MAX_UNSPACED_LINE_CHARS
            and keyword.text in candidate[:UNSPACED_HEADING_WINDOW]
        )
    return f" {keyword.text} " in f" {candidate} "
