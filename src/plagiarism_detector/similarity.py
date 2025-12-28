from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import List, Sequence, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass(frozen=True)
class SimilarityConfig:
    ngram_n: int = 3
    tfidf_ngram_range: Tuple[int, int] = (1, 2)
    weights: Tuple[float, float, float] = (0.55, 0.25, 0.20)  # (tfidf, sequence, ngram)


def sequence_ratio(a: str, b: str) -> float:
    return float(SequenceMatcher(None, a, b).ratio())


def word_ngrams(tokens: Sequence[str], n: int) -> List[Tuple[str, ...]]:
    if n <= 0:
        raise ValueError("n must be > 0")
    if len(tokens) < n:
        return []
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def ngram_jaccard(tokens_a: Sequence[str], tokens_b: Sequence[str], n: int = 3) -> float:
    A = set(word_ngrams(tokens_a, n))
    B = set(word_ngrams(tokens_b, n))
    if not A and not B:
        return 1.0
    if not A or not B:
        return 0.0
    return float(len(A & B) / len(A | B))


def cosine_tfidf_matrix(texts: List[str], ngram_range: Tuple[int, int] = (1, 2)) -> np.ndarray:
    if not texts:
        return np.zeros((0, 0), dtype=float)

    vec = TfidfVectorizer(ngram_range=ngram_range, min_df=1)

    try:
        X = vec.fit_transform(texts)
    except ValueError:
        # Например: все документы пустые -> empty vocabulary
        n = len(texts)
        sim = np.zeros((n, n), dtype=float)
        np.fill_diagonal(sim, 1.0)
        return sim

    sim = (X @ X.T).toarray()
    sim = np.clip(sim, 0.0, 1.0)
    np.fill_diagonal(sim, 1.0)
    return sim
