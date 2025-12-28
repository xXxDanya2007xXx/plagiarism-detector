from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import matplotlib.pyplot as plt

from .analyzer import AnalysisResult

plt.switch_backend("Agg")


def _off_diagonal_values(matrix: Sequence[Sequence[float]]) -> List[float]:
    vals: List[float] = []
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            vals.append(float(matrix[i][j]))
    return vals


def build_summary(result: AnalysisResult) -> Dict[str, Any]:
    vals = _off_diagonal_values(result.similarity_matrix)

    if not vals:
        return {
            "n_files": len(result.files),
            "n_pairs": 0,
            "pairs_above_threshold": 0,
            "max_pair_score": None,
            "mean_pair_score": None,
            "median_pair_score": None,
        }

    pairs_above = sum(1 for v in vals if v >= result.threshold)
    return {
        "n_files": len(result.files),
        "n_pairs": len(vals),
        "pairs_above_threshold": pairs_above,
        "max_pair_score": max(vals),
        "mean_pair_score": statistics.mean(vals),
        "median_pair_score": statistics.median(vals),
    }


def top_pairs_overall(
    files: Sequence[str],
    matrix: Sequence[Sequence[float]],
    *,
    k: int = 10,
) -> List[Dict[str, Any]]:
    pairs: List[Tuple[str, str, float]] = []
    n = len(files)
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((files[i], files[j], float(matrix[i][j])))

    pairs.sort(key=lambda x: x[2], reverse=True)
    out: List[Dict[str, Any]] = []
    for a, b, s in pairs[:k]:
        out.append({"a": a, "b": b, "score": round(float(s), 6)})
    return out


def save_json(result: AnalysisResult, path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "created_at_utc": result.created_at_utc,
        "files": result.files,
        "similarity_matrix": result.similarity_matrix,
        "top_pairs": result.top_pairs,  # pairs >= threshold (may be empty)
        "top_pairs_overall": top_pairs_overall(result.files, result.similarity_matrix, k=10),
        "threshold": result.threshold,
        "config": getattr(result, "config", {}),
        "summary": build_summary(result),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _pairs_table_columns(pairs: List[Dict[str, Any]]) -> List[str]:
    if not pairs:
        return ["a", "b", "score"]

    preferred = ["a", "b", "score", "tfidf", "sequence", "ngram", "lcs"]
    present = set()
    for p in pairs:
        present.update(p.keys())

    cols = [c for c in preferred if c in present]
    extras = sorted([k for k in present if k not in cols])
    return cols + extras


def _md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def _fmt(v: Any) -> str:
    if isinstance(v, float):
        return f"{v:.4f}"
    return str(v)


def _render_pairs_md(pairs: List[Dict[str, Any]]) -> str:
    if not pairs:
        return "_No pairs._\n"

    cols = _pairs_table_columns(pairs)
    lines: List[str] = []
    lines.append("| " + " | ".join(cols) + " |\n")
    lines.append("|" + "|".join(["---"] * len(cols)) + "|\n")
    for p in pairs:
        row = [_md_escape(_fmt(p.get(c, ""))) for c in cols]
        lines.append("| " + " | ".join(row) + " |\n")
    return "".join(lines)


def save_markdown(result: AnalysisResult, path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    summary = build_summary(result)
    cfg = getattr(result, "config", {})
    overall = top_pairs_overall(result.files, result.similarity_matrix, k=10)

    lines: List[str] = []
    lines.append("# Plagiarism Detector Report\n\n")
    lines.append(f"- Created (UTC): `{result.created_at_utc}`\n")
    lines.append(f"- Files: **{len(result.files)}**\n")
    lines.append(f"- Threshold: **{result.threshold:.2f}**\n\n")

    lines.append("## Summary\n\n")
    lines.append("| Metric | Value |\n|---|---:|\n")
    lines.append(f"| Files | {summary['n_files']} |\n")
    lines.append(f"| Pairs (off-diagonal) | {summary['n_pairs']} |\n")
    lines.append(f"| Pairs ≥ threshold | {summary['pairs_above_threshold']} |\n")
    if summary["max_pair_score"] is None:
        lines.append("| Max score | - |\n| Mean score | - |\n| Median score | - |\n")
    else:
        lines.append(f"| Max score | {summary['max_pair_score']:.4f} |\n")
        lines.append(f"| Mean score | {summary['mean_pair_score']:.4f} |\n")
        lines.append(f"| Median score | {summary['median_pair_score']:.4f} |\n")

    lines.append("\n## Top suspicious pairs\n\n")
    if not result.top_pairs:
        lines.append("_No pairs above threshold._\n")
    else:
        lines.append(_render_pairs_md(result.top_pairs))

    lines.append("\n## Top pairs (overall)\n\n")
    lines.append(_render_pairs_md(overall))

    lines.append("\n## Files\n\n")
    for f in result.files:
        lines.append(f"- `{_md_escape(f)}`\n")

    lines.append("\n## Config\n\n```json\n")
    lines.append(json.dumps(cfg, ensure_ascii=False, indent=2))
    lines.append("\n```\n")

    path.write_text("".join(lines), encoding="utf-8")


def save_heatmap_png(result: AnalysisResult, path: Path, *, title: str = "Similarity heatmap") -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    mat = result.similarity_matrix
    if not mat:
        return

    n = len(mat)
    fig_w = max(6.0, min(16.0, 0.65 * n + 4.0))
    fig_h = max(5.0, min(14.0, 0.65 * n + 3.0))

    plt.figure(figsize=(fig_w, fig_h))
    plt.imshow(mat, vmin=0.0, vmax=1.0, cmap="viridis")
    plt.colorbar(label="Similarity")
    plt.xticks(range(n), result.files, rotation=45, ha="right")
    plt.yticks(range(n), result.files)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def save_similarity_histogram_png(
    result: AnalysisResult,
    path: Path,
    *,
    bins: int = 20,
    title: str = "Similarity distribution (off-diagonal)",
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    vals = _off_diagonal_values(result.similarity_matrix)
    plt.figure(figsize=(8, 4.5))

    if not vals:
        plt.text(0.5, 0.5, "Not enough data", ha="center", va="center")
        plt.axis("off")
    else:
        plt.hist(vals, bins=bins, range=(0.0, 1.0), color="#2c7fb8", edgecolor="white")
        plt.axvline(result.threshold, color="#d95f0e", linestyle="--", linewidth=2)
        plt.xlabel("Similarity score")
        plt.ylabel("Count")
        plt.title(title)

    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def save_top_pairs_bar_png(
    result: AnalysisResult,
    path: Path,
    *,
    k: int = 10,
    title: str = "Top pairs (overall)",
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    pairs = top_pairs_overall(result.files, result.similarity_matrix, k=k)

    plt.figure(figsize=(10, 0.6 * max(1, len(pairs)) + 2.5))

    if not pairs:
        plt.text(0.5, 0.5, "No pairs", ha="center", va="center")
        plt.axis("off")
    else:
        labels = [f"{p['a']} ↔ {p['b']}" for p in reversed(pairs)]
        scores = [float(p["score"]) for p in reversed(pairs)]
        plt.barh(labels, scores, color="#41ab5d")
        plt.xlim(0.0, 1.0)
        plt.xlabel("Similarity score")
        plt.title(title)

    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
