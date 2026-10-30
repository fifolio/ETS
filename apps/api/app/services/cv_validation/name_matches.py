from app.services.text.has_unspaced_script import has_unspaced_script
from app.services.text.normalize import normalize


def name_matches(text: str, account_name: str) -> bool:
    parts = [part for part in normalize(account_name).split() if len(part) >= 2]
    if not parts:
        return True  # nothing reliable to compare against
    required = len(parts) if len(parts) <= 2 else len(parts) - 1
    normalized_cv = normalize(text)
    cv_words = set(normalized_cv.split())

    def appears(part: str) -> bool:
        if has_unspaced_script(part):
            return part in normalized_cv  # Chinese, Japanese, Thai names have no spaces around
        return part in cv_words

    return sum(appears(part) for part in parts) >= required
