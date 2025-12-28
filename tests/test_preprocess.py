from plagiarism_detector.preprocess import tokenize


def test_tokenize_basic():
    tokens = tokenize("Hello, world! Hello!!!")
    assert tokens.count("hello") == 2
    assert "world" in tokens
