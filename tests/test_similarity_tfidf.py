import numpy as np

from plagiarism_detector.similarity import cosine_tfidf_matrix


def test_tfidf_matrix_shape_and_diag():
    texts = [
        "alpha beta gamma",
        "alpha beta gamma",
        "delta epsilon zeta",
    ]
    m = cosine_tfidf_matrix(texts)
    assert m.shape == (3, 3)
    assert np.allclose(np.diag(m), 1.0)
    assert m[0, 1] > m[0, 2]
