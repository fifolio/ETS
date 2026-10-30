from app.constants.cv_validation import EMAIL_PATTERN


def email_problem(text: str, account_email: str) -> str | None:
    if account_email.lower() in text.lower():
        return None
    if not EMAIL_PATTERN.search(text):
        return "No email address found on the CV. Add the email you signed up with."
    return (
        "The CV doesn't contain your account email address. "
        "Add it to your CV, or sign up with the email shown on it."
    )
