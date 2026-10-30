import json
from pathlib import Path

import pytest

from app.chains.analyze import analyze

DATA = Path(__file__).resolve().parents[4] / "data"
CASES = json.loads((DATA / "cases.json").read_text())


@pytest.mark.eval
@pytest.mark.parametrize("case", CASES, ids=lambda c: c["job"])
def test_verdict_matches_expected(case):
    cv = (DATA / case["cv"]).read_text(encoding="utf-8")
    job = (DATA / case["job"]).read_text(encoding="utf-8")
    result = analyze(cv, job)
    assert result.verdict == case["expected"]


# @pytest.mark.eval
# def test_verdict_matches_expected():
#     for case in CASES:
#         cv = (DATA / case["cv"]).read_text(encoding="utf-8")
#         job = (DATA / case["job"]).read_text(encoding="utf-8")
#         result = analyze(cv, job)
#     assert result.verdict == case["expected"]
