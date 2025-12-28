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
    max_lcs_tokens: int = 2000
    weights: Tuple[float, float, float, float] = (0.45, 0.20, 0.20, 0.15)
    # (tfidf, sequence, ngram_jaccard, lcs)


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
        # empty vocabulary (e.g., all docs are empty)
        n = len(texts)
        sim = np.zeros((n, n), dtype=float)
        np.fill_diagonal(sim, 1.0)
        return sim

    sim = (X @ X.T).toarray()
    sim = np.clip(sim, 0.0, 1.0)
    np.fill_diagonal(sim, 1.0)
    return sim


def lcs_length(a: Sequence[str], b: Sequence[str]) -> int:
    # O(min(n,m)) memory DP
    if len(a) < len(b):
        a, b = b, a
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0]
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            if ai == b[j - 1]:
                cur.append(prev[j - 1] + 1)
            else:
                cur.append(max(prev[j], cur[-1]))
        prev = cur
    return prev[-1]


def lcs_similarity(tokens_a: Sequence[str], tokens_b: Sequence[str], *, max_tokens: int = 2000) -> float:
    a = list(tokens_a[:max_tokens])
    b = list(tokens_b[:max_tokens])
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    lcs_len = lcs_length(a, b)
    return float(2.0 * lcs_len / (len(a) + len(b)))
