from pathlib import Path

from src.pipeline import run_pipeline


def test_pipeline_generates_report(tmp_path: Path) -> None:
    output = tmp_path / "audit.md"
    report = run_pipeline("data/sample_transcript.txt", "controls/controls.yaml", str(output))

    assert output.exists()
    assert "Compliance Audit Report" in report
    assert "SOC2-CC6.1" in report
    assert "GDPR-ART32" in report
