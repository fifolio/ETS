import json
from pathlib import Path


def read_language_file(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
