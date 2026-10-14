import runpy
from pathlib import Path


def test_published_integrity_replay_preserves_decisions_and_missingness():
    root = Path(__file__).resolve().parents[1]
    report = runpy.run_path(str(root / "evaluation/integrity.py"))["build_integrity_report"]()
    cases = {c["id"]: c for c in report["cases"]}
    assert all(c["matches_expectation"] for c in cases.values())
    assert cases["valid_same_platform"]["result"]["readiness"] == "blocked"
    assert cases["conflicting_reports"]["result"]["device_check"] == "unknown"
    assert cases["conflicting_reports"]["result"]["readiness"] == "needs_evidence"
    assert "sdk_version" in cases["empty_detail"]["result"]["ticket_missing_fields"]
