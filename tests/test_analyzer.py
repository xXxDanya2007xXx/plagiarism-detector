from pathlib import Path

from plagiarism_detector.analyzer import analyze_folder


def test_analyze_folder_tmp(tmp_path: Path):
    (tmp_path / "a.txt").write_text("This is a test text about Python.", encoding="utf-8")
    (tmp_path / "b.txt").write_text("This is a test text about Python and code.", encoding="utf-8")

    result = analyze_folder(tmp_path, threshold=0.1)
    assert len(result.files) == 2
    assert len(result.similarity_matrix) == 2
    assert result.similarity_matrix[0][0] == 1.0
    assert result.similarity_matrix[1][1] == 1.0
