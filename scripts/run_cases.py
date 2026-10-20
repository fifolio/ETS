import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api"))

from app.chains.matcher import analyze  # noqa: E402

DATA = ROOT / "data"


def main():
    cases = json.loads((DATA / "cases.json").read_text())
    for case in cases:
        cv = (DATA / case["cv"]).read_text()
        job = (DATA / case["job"]).read_text()
        result = analyze(cv, job)
        mark = "OK " if result.verdict == case["expected"] else "BAD"
        print(f"[{mark}] {case['job']}: {result.verdict} ({result.score}), expected {case['expected']}")
        print(f"      {result.summary}")
        if result.red_flags:
            print(f"      red flags: {result.red_flags}")


if __name__ == "__main__":
    main()