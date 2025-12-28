from plagiarism_detector.similarity import ngram_jaccard


def test_ngram_jaccard_identity():
    t = "a b c d e".split()
    assert ngram_jaccard(t, t, n=3) == 1.0
