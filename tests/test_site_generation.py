from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def test_generate_site_script(tmp_path: Path):
    (tmp_path / "a.txt").write_text("alpha beta gamma alpha beta", encoding="utf-8")
    (tmp_path / "b.txt").write_text("alpha beta delta alpha beta", encoding="utf-8")

    out = tmp_path / "reports"
    site = tmp_path / "site"

    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "scripts" / "generate_site.py"

    subprocess.check_call(
        [
            sys.executable,
            str(script),
            "--input",
            str(tmp_path),
            "--out",
            str(out),
            "--site",
            str(site),
            "--threshold",
            "0.1",
        ]
    )

    assert (site / "index.html").exists()
    html = (site / "index.html").read_text(encoding="utf-8")
    assert "<title>Plagiarism Detector Report</title>" in html
    assert "report.json" in html
    assert "report.md" in html
