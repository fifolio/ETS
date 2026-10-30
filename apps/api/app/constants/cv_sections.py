from pathlib import Path

# Folder with one JSON file of CV section headings per language
SECTIONS_DIR = Path(__file__).resolve().parent.parent / "resources" / "cv_sections"
SECTION_NAMES = ("education", "experience", "skills", "profile")
