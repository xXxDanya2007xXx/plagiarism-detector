from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .preprocess import PreprocessConfig, tokenize
from .readers import read_folder
from .similarity import SimilarityConfig, combined_similarity


@dataclass(frozen=True)
class AnalysisResult:
    created_at_utc: str
    files: List[str]
    similarity_matrix: List[List[float]]
    top_pairs: List[Dict[str, Any]]
    threshold: float


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

    if not docs:
        return AnalysisResult(
            created_at_utc=created,
            files=[],
            similarity_matrix=[],
            top_pairs=[],
            threshold=float(threshold),
        )

    tokens = [tokenize(d.text, preprocess_cfg) for d in docs]
    texts = [d.text for d in docs]

    n = len(docs)
    mat: List[List[float]] = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        mat[i][i] = 1.0
        for j in range(i + 1, n):
            s = combined_similarity(texts[i], texts[j], tokens[i], tokens[j], sim_cfg)
            s = round(float(s), 6)
            mat[i][j] = s
            mat[j][i] = s

    pairs: List[Dict[str, Any]] = []
    for i in range(n):
        for j in range(i + 1, n):
            if mat[i][j] >= threshold:
                pairs.append({"a": files[i], "b": files[j], "score": mat[i][j]})
    pairs.sort(key=lambda x: x["score"], reverse=True)

    return AnalysisResult(
        created_at_utc=created,
        files=files,
        similarity_matrix=mat,
        top_pairs=pairs[:10],
        threshold=float(threshold),
    )


def save_result_json(result: AnalysisResult, out_path: Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "created_at_utc": result.created_at_utc,
        "files": result.files,
        "similarity_matrix": result.similarity_matrix,
        "top_pairs": result.top_pairs,
        "threshold": result.threshold,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
