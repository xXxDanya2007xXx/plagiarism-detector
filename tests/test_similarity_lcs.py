from plagiarism_detector.similarity import lcs_similarity


def test_lcs_similarity_identity():
    t = "alpha beta gamma".split()
    assert lcs_similarity(t, t, max_tokens=100) == 1.0


def test_lcs_similarity_disjoint():
    a = "alpha beta".split()
    b = "gamma delta".split()
    assert lcs_similarity(a, b, max_tokens=100) == 0.0
