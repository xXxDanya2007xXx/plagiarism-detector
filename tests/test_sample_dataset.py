from pathlib import Path

from plagiarism_detector.analyzer import analyze_folder


def test_sample_dataset_exists():
    root = Path(__file__).resolve().parents[1]
    sample_dir = root / "data" / "sample"
    txts = list(sample_dir.glob("*.txt"))
    assert len(txts) >= 3


def test_analyze_sample_dataset_runs():
    root = Path(__file__).resolve().parents[1]
    sample_dir = root / "data" / "sample"

    result = analyze_folder(sample_dir, threshold=0.0)
    assert len(result.files) >= 3
    assert len(result.similarity_matrix) == len(result.files)
