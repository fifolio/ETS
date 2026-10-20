import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.services.cv_parser import extract_text_from_pdf

if __name__ == "__main__":
    print(extract_text_from_pdf(Path(sys.argv[1]).read_bytes()))

