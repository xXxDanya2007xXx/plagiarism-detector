from pathlib import Path

from plagiarism_detector.analyzer import analyze_folder
from plagiarism_detector.reporting import save_json, save_markdown, save_heatmap_png


def test_reporting_creates_files(tmp_path: Path):
    (tmp_path / "a.txt").write_text("alpha beta gamma", encoding="utf-8")
    (tmp_path / "b.txt").write_text("alpha beta delta", encoding="utf-8")

    result = analyze_folder(tmp_path, threshold=0.1)

    out = tmp_path / "out"
    save_json(result, out / "report.json")
    save_markdown(result, out / "report.md")
    save_heatmap_png(result, out / "heatmap.png")

    assert (out / "report.json").exists()
    assert (out / "report.md").exists()
    # heatmap может не создаться если матрица пустая; тут она не пустая
    assert (out / "heatmap.png").exists()
