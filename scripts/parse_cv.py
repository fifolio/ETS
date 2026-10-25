import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.services.cv_parser import extract_text_from_pdf
from app.services.cv_validator import validate_cv


if __name__ == "__main__":
    text = extract_text_from_pdf(Path(sys.argv[1]).read_bytes())
    print(text)
    if len(sys.argv) == 4:
        problems = validate_cv(text, account_name=sys.argv[2], account_email=sys.argv[3])
        print("\n--- validation ---")
        print("OK" if not problems else "\n".join(problems))