from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

from .analyzer import AnalysisResult

# Safe for CI/headless environments; no E402 because all imports are above.
plt.switch_backend("Agg")


def save_json(result: AnalysisResult, path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "created_at_utc": result.created_at_utc,
        "files": result.files,
        "similarity_matrix": result.similarity_matrix,
        "top_pairs": result.top_pairs,
        "threshold": result.threshold,
        "config": result.config,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def save_markdown(result: AnalysisResult, path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("# Plagiarism Detector Report\n\n")
    lines.append(f"- Created (UTC): `{result.created_at_utc}`\n")
    lines.append(f"- Files: **{len(result.files)}**\n")
    lines.append(f"- Threshold: **{result.threshold:.2f}**\n\n")

    lines.append("## Top suspicious pairs\n\n")
    if not result.top_pairs:
        lines.append("_No pairs above threshold._\n")
    else:
        lines.append("| A | B | Score |\n|---|---|---:|\n")
        for p in result.top_pairs:
            lines.append(f"| `{p['a']}` | `{p['b']}` | {p['score']:.4f} |\n")

    lines.append("\n## Files\n\n")
    for f in result.files:
        lines.append(f"- `{f}`\n")

    path.write_text("".join(lines), encoding="utf-8")


def save_heatmap_png(
    result: AnalysisResult, path: Path, *, title: str = "Similarity heatmap"
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    mat = result.similarity_matrix
    if not mat:
        # нечего рисовать
        return

    n = len(mat)
    fig_w = max(6, min(14, 0.6 * n + 4))
    fig_h = max(5, min(12, 0.6 * n + 3))

    plt.figure(figsize=(fig_w, fig_h))
    plt.imshow(mat, vmin=0.0, vmax=1.0, cmap="viridis")
    plt.colorbar(label="Similarity")

    plt.xticks(range(n), result.files, rotation=45, ha="right")
    plt.yticks(range(n), result.files)

    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
