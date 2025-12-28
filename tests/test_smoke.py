import plagiarism_detector


def test_version_exists():
    assert isinstance(plagiarism_detector.__version__, str)
    assert plagiarism_detector.__version__
