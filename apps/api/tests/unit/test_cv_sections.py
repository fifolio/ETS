import json

import pytest

from app.services import cv_sections
from app.services.cv_sections import SECTION_NAMES, SECTIONS_DIR, load_keywords
from app.services.cv_validator import find_sections


@pytest.fixture
def sections_dir(tmp_path, monkeypatch):
    """Point the loader at an empty temporary folder, then restore the real one."""
    monkeypatch.setattr(cv_sections, "SECTIONS_DIR", tmp_path)
    load_keywords.cache_clear()
    yield tmp_path
    load_keywords.cache_clear()


@pytest.mark.parametrize("path", sorted(SECTIONS_DIR.glob("*.json")), ids=lambda path: path.stem)
def test_language_file_is_valid(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(data.get("language"), str), f"{path.name}: 'language' is missing"
    for section in SECTION_NAMES:
        words = data.get(section)
        assert isinstance(words, list) and words, f"{path.name}: '{section}' must not be empty"
        assert all(isinstance(word, str) and word.strip() for word in words)


def test_bundled_language_files_load_without_conflicts():
    assert load_keywords()


def test_a_new_language_file_is_picked_up_without_code_changes(sections_dir):
    german = {
        "language": "German",
        "education": ["ausbildung"],
        "experience": ["berufserfahrung"],
        "skills": ["kenntnisse"],
        "profile": ["profil"],
    }
    (sections_dir / "de.json").write_text(json.dumps(german), encoding="utf-8")

    assert find_sections("Berufserfahrung\nsome content here") == {"experience"}


def test_conflicting_files_are_rejected(sections_dir):
    base = {
        "language": "A",
        "education": ["alpha"],
        "experience": ["beta"],
        "skills": ["gamma"],
        "profile": ["delta"],
    }
    clash = {**base, "language": "B", "education": ["omega"], "skills": ["alpha"]}
    (sections_dir / "a.json").write_text(json.dumps(base), encoding="utf-8")
    (sections_dir / "b.json").write_text(json.dumps(clash), encoding="utf-8")

    with pytest.raises(ValueError, match="alpha"):
        load_keywords()
