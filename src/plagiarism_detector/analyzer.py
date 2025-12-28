from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

from .preprocess import PreprocessConfig, detokenize, tokenize
from .readers import read_folder
from .similarity import SimilarityConfig, cosine_tfidf_matrix, ngram_jaccard, sequence_ratio


@dataclass(frozen=True)
class AnalysisResult:
    created_at_utc: str
    files: List[str]
    similarity_matrix: List[List[float]]
    top_pairs: List[Dict[str, Any]]
    threshold: float
    config: Dict[str, Any]


def analyze_folder(
    folder: Path,
    *,
    threshold: float = 0.75,
    preprocess_cfg: PreprocessConfig = PreprocessConfig(),
    sim_cfg: SimilarityConfig = SimilarityConfig(),
) -> AnalysisResult:
    docs = read_folder(Path(folder))
    files = [d.name for d in docs]
    created = datetime.now(timezone.utc).isoformat(timespec="seconds")

    cfg_dump: Dict[str, Any] = {
        "preprocess": asdict(preprocess_cfg),
        "similarity": asdict(sim_cfg),
    }

    if not docs:
        return AnalysisResult(
            created_at_utc=created,
            files=[],
            similarity_matrix=[],
            top_pairs=[],
            threshold=float(threshold),
            config=cfg_dump,
        )

    tokens = [tokenize(d.text, preprocess_cfg) for d in docs]
    texts_for_tfidf = [detokenize(t) for t in tokens]
    original_texts = [d.text for d in docs]

    tfidf = cosine_tfidf_matrix(texts_for_tfidf, ngram_range=sim_cfg.tfidf_ngram_range)
    n = len(docs)

    w_tfidf, w_seq, w_ng = sim_cfg.weights
    mat = np.zeros((n, n), dtype=float)
    np.fill_diagonal(mat, 1.0)

    for i in range(n):
        for j in range(i + 1, n):
            s_seq = sequence_ratio(original_texts[i], original_texts[j])
            s_ng = ngram_jaccard(tokens[i], tokens[j], n=sim_cfg.ngram_n)
            s = w_tfidf * float(tfidf[i, j]) + w_seq * s_seq + w_ng * s_ng
            s = float(np.clip(s, 0.0, 1.0))
            mat[i, j] = s
            mat[j, i] = s

    pairs: List[Dict[str, Any]] = []
    for i in range(n):
        for j in range(i + 1, n):
            score = float(mat[i, j])
            if score >= threshold:
                pairs.append({"a": files[i], "b": files[j], "score": round(score, 6)})
    pairs.sort(key=lambda x: x["score"], reverse=True)

    return AnalysisResult(
        created_at_utc=created,
        files=files,
        similarity_matrix=[[round(float(x), 6) for x in row] for row in mat.tolist()],
        top_pairs=pairs[:10],
        threshold=float(threshold),
        config=cfg_dump,
    )
