from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import List, Sequence, Tuple


@dataclass(frozen=True)
class SimilarityConfig:
    ngram_n: int = 3
    weights: Tuple[float, float] = (0.6, 0.4)  # (sequence, ngram_jaccard)


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


def combined_similarity(
    text_a: str,
    text_b: str,
    tokens_a: Sequence[str],
    tokens_b: Sequence[str],
    cfg: SimilarityConfig = SimilarityConfig(),
) -> float:
    w_seq, w_ng = cfg.weights
    s = w_seq * sequence_ratio(text_a, text_b) + w_ng * ngram_jaccard(
        tokens_a, tokens_b, n=cfg.ngram_n
    )
    return float(min(1.0, max(0.0, s)))
