import pytest

from app.services.cv_validator import find_sections, validate_cv

GOOD_CV = """
Jane Doe
jane.doe@example.com | +1 555 0100

Profile
Frontend developer with two years of experience building web apps.

Experience
Frontend Developer, Acme (2023-2025)

Education
BSc Computer Science, Example University

Skills
React, TypeScript, Tailwind CSS
"""

ACCOUNT = {"account_name": "Jane Doe", "account_email": "jane.doe@example.com"}


def test_accepts_a_complete_cv():
    assert validate_cv(GOOD_CV, **ACCOUNT) == []


def test_rejects_cv_without_the_account_email():
    problems = validate_cv(GOOD_CV, account_name="Jane Doe", account_email="other@example.com")
    assert len(problems) == 1
    assert "email" in problems[0]


def test_reports_when_the_cv_has_no_email_at_all():
    cv = GOOD_CV.replace("jane.doe@example.com", "")
    problems = validate_cv(cv, **ACCOUNT)
    assert len(problems) == 1
    assert "No email address" in problems[0]


def test_email_match_ignores_case():
    cv = GOOD_CV.replace("jane.doe@example.com", "Jane.Doe@Example.com")
    assert validate_cv(cv, **ACCOUNT) == []


def test_name_match_ignores_accents_and_case():
    cv = GOOD_CV.replace("Jane Doe", "JEANNE DUPRE")
    result = validate_cv(cv, account_name="Jeanne Dupré", account_email="jane.doe@example.com")
    assert result == []


def test_rejects_a_different_name():
    problems = validate_cv(GOOD_CV, account_name="John Smith", account_email="jane.doe@example.com")
    assert len(problems) == 1
    assert "name" in problems[0]


def test_three_part_name_allows_one_missing_part():
    result = validate_cv(
        GOOD_CV, account_name="Jane Marie Doe", account_email="jane.doe@example.com"
    )
    assert result == []


def test_two_part_name_needs_both_parts():
    problems = validate_cv(GOOD_CV, account_name="Jane Smith", account_email="jane.doe@example.com")
    assert len(problems) == 1


def test_name_check_when_the_account_has_no_name():
    cv = GOOD_CV.replace("Jane Doe", "Anonymous")
    assert validate_cv(cv, account_name="", account_email="jane.doe@example.com") == [
        "The CV doesn't contain your account name. "
        "Make sure the name on your CV matches the name you signed up with."
    ]


def test_rejects_text_without_any_section():
    cv = (
        "Jane Doe\njane.doe@example.com\n"
        "This is just a page of random words without any structure at all."
    )
    problems = validate_cv(cv, **ACCOUNT)
    assert len(problems) == 1
    assert "section" in problems[0]


@pytest.mark.parametrize(
    ("heading", "expected"),
    [
        ("Compétences", "skills"),
        ("Formation", "education"),
        ("Expérience professionnelle", "experience"),
        ("PROFIL", "profile"),
        ("Technical Skills", "skills"),
        ("Work Experience", "experience"),
    ],
)
def test_finds_headings_in_english_and_french(heading, expected):
    assert find_sections(f"{heading}\nsome content here") == {expected}


def test_inline_heading_with_a_colon_counts():
    assert find_sections("Skills: React, TypeScript, Tailwind CSS, Docker") == {"skills"}


def test_a_sentence_mentioning_experience_is_not_a_heading():
    text = "I have a lot of experience with many different programming languages."
    assert find_sections(text) == set()


def test_reports_every_problem_at_once():
    problems = validate_cv("random text", **ACCOUNT)
    assert len(problems) == 3  # email, name, and sections


@pytest.mark.parametrize(
    ("heading", "expected"),
    [
        ("Educación", "education"),
        ("Experiencia laboral", "experience"),
        ("Habilidades", "skills"),
        ("الخبرة العملية", "experience"),
        ("المهارات", "skills"),
        ("教育背景", "education"),
        ("技能：React、Node.js", "skills"),
    ],
)
def test_finds_headings_in_spanish_arabic_and_chinese(heading, expected):
    assert find_sections(f"{heading}\nsome content here") == {expected}


def test_a_long_chinese_sentence_is_not_a_heading():
    text = "我有很多教育方面的经验可以分享给大家，希望大家喜欢这个项目的设计和实现过程"
    assert find_sections(text) == set()


def test_chinese_name_matches_without_spaces():
    cv = "姓名：张伟 | zhang@example.com\n教育背景\n北京大学计算机系"
    assert validate_cv(cv, account_name="张伟", account_email="zhang@example.com") == []
