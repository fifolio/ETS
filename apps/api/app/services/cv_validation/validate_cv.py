from app.services.cv_validation.email_problem import email_problem
from app.services.cv_validation.find_sections import find_sections
from app.services.cv_validation.name_matches import name_matches


def validate_cv(text: str, *, account_name: str, account_email: str) -> list[str]:
    """Return a list of problems with the CV. An empty list means it's accepted."""
    problems = []

    problem = email_problem(text, account_email)
    if problem:
        problems.append(problem)

    if not name_matches(text, account_name):
        problems.append("The CV doesn't contain your account name.")

    if not find_sections(text):
        problems.append(
            "No Education, Experience, Skills, or Profile section found. "
            "Make sure at least one of these headings appears in your CV."
        )

    return problems
