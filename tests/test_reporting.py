from __future__ import annotations

import json
from pathlib import Path

from plagiarism_detector.analyzer import analyze_folder
from plagiarism_detector.reporting import (
    save_heatmap_png,
    save_json,
    save_markdown,
    save_similarity_histogram_png,
    save_top_pairs_bar_png,
)


def test_reporting_creates_files(tmp_path: Path):
    (tmp_path / "a.txt").write_text("alpha beta gamma alpha beta", encoding="utf-8")
    (tmp_path / "b.txt").write_text("alpha beta delta alpha beta", encoding="utf-8")
    (tmp_path / "c.txt").write_text("completely different topic words here", encoding="utf-8")

    result = analyze_folder(tmp_path, threshold=0.75)

    out = tmp_path / "out"
    out.mkdir(parents=True, exist_ok=True)

    save_json(result, out / "report.json")
    save_markdown(result, out / "report.md")
    save_heatmap_png(result, out / "heatmap.png")
    save_similarity_histogram_png(result, out / "similarity_hist.png")
    save_top_pairs_bar_png(result, out / "top_pairs.png")

    assert (out / "report.json").exists()
    assert (out / "report.md").exists()
    assert (out / "heatmap.png").exists()
    assert (out / "similarity_hist.png").exists()
    assert (out / "top_pairs.png").exists()

    payload = json.loads((out / "report.json").read_text(encoding="utf-8"))
    for key in [
        "created_at_utc",
        "files",
        "similarity_matrix",
        "top_pairs",
        "top_pairs_overall",
        "threshold",
        "config",
        "summary",
    ]:
        assert key in payload

    md_text = (out / "report.md").read_text(encoding="utf-8")
    assert "# Plagiarism Detector Report" in md_text
    assert "## Summary" in md_text
    assert "## Top suspicious pairs" in md_text
    assert "## Top pairs (overall)" in md_text
    assert "## Config" in md_text
