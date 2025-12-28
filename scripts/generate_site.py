from __future__ import annotations

import argparse
import inspect
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import markdown as md

from plagiarism_detector.analyzer import analyze_folder

# Core reporting functions (must exist)
from plagiarism_detector.reporting import build_summary, save_heatmap_png, save_json, save_markdown

# Optional chart functions (may not exist yet in your reporting.py)
try:
    from plagiarism_detector.reporting import (  # type: ignore
        save_similarity_histogram_png,
        save_top_pairs_bar_png,
    )
except Exception:  # pragma: no cover
    save_similarity_histogram_png = None  # type: ignore
    save_top_pairs_bar_png = None  # type: ignore

# Optional helper to compute overall pairs (may not exist yet in your reporting.py)
try:
    from plagiarism_detector.reporting import top_pairs_overall  # type: ignore
except Exception:  # pragma: no cover
    top_pairs_overall = None  # type: ignore


def _html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")


def _format_cell(v: Any) -> str:
    if isinstance(v, float):
        return f"{v:.4f}"
    return str(v)


def _parse_exts(value: str) -> Optional[List[str]]:
    v = value.strip()
    if not v:
        return None
    parts = [p.strip() for p in v.split(",")]
    return [p for p in parts if p]


def _pairs_table_html(pairs: List[Dict[str, Any]]) -> str:
    if not pairs:
        return "<p><em>No pairs to show.</em></p>"

    preferred = ["a", "b", "score", "tfidf", "sequence", "ngram", "lcs"]
    present = set()
    for p in pairs:
        present.update(p.keys())

    cols = [c for c in preferred if c in present]
    cols += sorted([k for k in present if k not in preferred])

    head = "".join(f"<th>{_html_escape(c)}</th>" for c in cols)

    rows: List[str] = []
    for p in pairs:
        tds: List[str] = []
        for c in cols:
            cell = _format_cell(p.get(c, ""))
            tds.append(f"<td>{_html_escape(cell)}</td>")
        rows.append("<tr>" + "".join(tds) + "</tr>")

    return "<table>" f"<thead><tr>{head}</tr></thead>" f"<tbody>{''.join(rows)}</tbody>" "</table>"


def _matrix_table_html(files: Sequence[str], matrix: Sequence[Sequence[float]]) -> str:
    n = len(files)
    if n == 0 or n != len(matrix):
        return "<p><em>No matrix available.</em></p>"

    thead = "<th></th>" + "".join(f"<th>{_html_escape(name)}</th>" for name in files)

    body_rows: List[str] = []
    for i in range(n):
        row_cells: List[str] = [f"<th>{_html_escape(files[i])}</th>"]
        for j in range(n):
            v = float(matrix[i][j])
            row_cells.append(f"<td style='text-align:right'>{v:.3f}</td>")
        body_rows.append("<tr>" + "".join(row_cells) + "</tr>")

    return (
        "<div style='overflow:auto; border:1px solid #eee; border-radius:10px;'>"
        "<table style='margin:0; min-width:700px;'>"
        f"<thead><tr>{thead}</tr></thead>"
        f"<tbody>{''.join(body_rows)}</tbody>"
        "</table>"
        "</div>"
    )


def _compute_overall_pairs(
    files: Sequence[str],
    matrix: Sequence[Sequence[float]],
    k: int = 10,
) -> List[Dict[str, Any]]:
    if top_pairs_overall is not None:
        return top_pairs_overall(files, matrix, k=k)

    # fallback: compute locally
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


def _copy_if_exists(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return True


def _write_site(
    site_dir: Path,
    report_md: Path,
    report_json: Path,
    *,
    payload: Dict[str, Any],
) -> None:
    site_dir.mkdir(parents=True, exist_ok=True)

    # Copy raw artifacts for download
    md_text = report_md.read_text(encoding="utf-8")
    (site_dir / "report.md").write_text(md_text, encoding="utf-8")
    (site_dir / "report.json").write_text(
        report_json.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    # Copy images if present (from reports/)
    heatmap_ok = _copy_if_exists(report_md.parent / "heatmap.png", site_dir / "heatmap.png")
    hist_ok = _copy_if_exists(
        report_md.parent / "similarity_hist.png",
        site_dir / "similarity_hist.png",
    )
    top_ok = _copy_if_exists(report_md.parent / "top_pairs.png", site_dir / "top_pairs.png")

    # Render markdown with code fences
    body_html = md.markdown(md_text, extensions=["tables", "fenced_code"])

    created_at = str(payload.get("created_at_utc", ""))
    threshold = float(payload.get("threshold", 0.0))
    summary = payload.get("summary") or {}

    summary_html = (
        "<div class='cards'>"
        "<div class='card'><div class='k'>Created (UTC)</div>"
        f"<div class='v small'>{_html_escape(created_at)}</div></div>"
        "<div class='card'><div class='k'>Threshold</div>"
        f"<div class='v'>{threshold:.2f}</div></div>"
        "<div class='card'><div class='k'>Files</div>"
        f"<div class='v'>{summary.get('n_files', '-')}</div></div>"
        "<div class='card'><div class='k'>Pairs</div>"
        f"<div class='v'>{summary.get('n_pairs', '-')}</div></div>"
        "<div class='card'><div class='k'>Pairs ≥ threshold</div>"
        f"<div class='v'>{summary.get('pairs_above_threshold', '-')}</div></div>"
        "<div class='card'><div class='k'>Max score</div>"
        f"<div class='v'>{_format_cell(summary.get('max_pair_score', '-'))}</div></div>"
        "</div>"
    )

    files = payload.get("files") or []
    matrix = payload.get("similarity_matrix") or []

    pairs_for_page = payload.get("top_pairs") or payload.get("top_pairs_overall") or []
    if not pairs_for_page:
        pairs_for_page = _compute_overall_pairs(files, matrix, k=10)

    pairs_html = _pairs_table_html(pairs_for_page)

    if 0 < len(files) <= 20:
        matrix_html = _matrix_table_html(files, matrix)
    else:
        matrix_html = (
            "<p class='muted'><em>" "Matrix table is shown only when N ≤ 20 (use heatmap for larger sets)." "</em></p>"
        )

    heatmap_block = "<p><em>No heatmap available.</em></p>"
    if heatmap_ok:
        heatmap_block = '<img src="heatmap.png" alt="Similarity heatmap"/>'

    hist_block = "<p><em>No similarity histogram available.</em></p>"
    if hist_ok:
        hist_block = '<img src="similarity_hist.png" alt="Similarity distribution"/>'

    top_block = "<p><em>No top-pairs chart available.</em></p>"
    if top_ok:
        top_block = '<img src="top_pairs.png" alt="Top pairs chart"/>'

    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Plagiarism Detector Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 1100px; margin: 2rem auto; padding: 0 1rem; }}
    a {{ color: #0b63ce; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .muted {{ color: #666; }}
    img {{ max-width: 100%; height: auto; border: 1px solid #eee; border-radius: 10px; }}
    .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 14px 0 18px; }}
    .card {{ border: 1px solid #eee; border-radius: 12px; padding: 12px; background: #fff; }}
    .card .k {{ font-size: 12px; color: #666; }}
    .card .v {{ font-size: 20px; font-weight: 700; margin-top: 4px; }}
    .card .v.small {{ font-size: 14px; font-weight: 600; }}
    table {{ border-collapse: collapse; width: 100%; margin: 10px 0 18px; }}
    th, td {{ border: 1px solid #e5e5e5; padding: 8px; }}
    th {{ background: #fafafa; text-align: left; }}
    pre {{ background: #f7f7f7; padding: 12px; border-radius: 10px; overflow: auto; }}
    code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 4px; }}
    h1 {{ margin: 0 0 6px 0; }}
  </style>
</head>
<body>
  <h1>Plagiarism Detector</h1>
  <div class="muted" style="margin-bottom:10px;">Static report page</div>

  <p>
    <a href="report.json">report.json</a> •
    <a href="report.md">report.md</a>
  </p>

  {summary_html}

  <h2>Top pairs</h2>
  <p class="muted">
    Showing the most similar pairs (overall). If threshold-filtered list is empty,
    this section is still populated.
  </p>
  {pairs_html}

  <h2>Matrix</h2>
  {matrix_html}

  <h2>Heatmap</h2>
  {heatmap_block}

  <h2>Charts</h2>
  <h3>Similarity distribution</h3>
  {hist_block}
  <h3>Top pairs (overall)</h3>
  {top_block}

  <h2>Full report</h2>
  {body_html}

</body>
</html>
"""
    (site_dir / "index.html").write_text(html, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="uploads", help="Folder with submissions")
    ap.add_argument("--out", default="reports", help="Output folder for reports")
    ap.add_argument("--site", default="site", help="Output folder for static site")
    ap.add_argument("--threshold", type=float, default=0.75, help="Suspicion threshold 0..1")
    ap.add_argument(
        "--exts",
        default="",
        help="Comma-separated extensions (used only if analyzer supports it)",
    )
    ap.add_argument(
        "--no-recursive",
        action="store_true",
        help="Do not scan subfolders (used only if analyzer supports it)",
    )
    ap.add_argument(
        "--clean-site",
        action="store_true",
        help="Remove existing site/ directory content before generation",
    )
    args = ap.parse_args()

    out_dir = Path(args.out)
    site_dir = Path(args.site)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.clean_site and site_dir.exists():
        shutil.rmtree(site_dir)

    sig = inspect.signature(analyze_folder)
    kwargs: Dict[str, Any] = {"threshold": float(args.threshold)}

    exts = _parse_exts(args.exts)
    if "exts" in sig.parameters:
        kwargs["exts"] = exts
    if "recursive" in sig.parameters:
        kwargs["recursive"] = not bool(args.no_recursive)

    result = analyze_folder(Path(args.input), **kwargs)

    report_json = out_dir / "report.json"
    report_md = out_dir / "report.md"
    heatmap_png = out_dir / "heatmap.png"
    hist_png = out_dir / "similarity_hist.png"
    top_png = out_dir / "top_pairs.png"

    save_json(result, report_json)
    save_markdown(result, report_md)
    save_heatmap_png(result, heatmap_png)

    if save_similarity_histogram_png is not None:
        save_similarity_histogram_png(result, hist_png)
    if save_top_pairs_bar_png is not None:
        save_top_pairs_bar_png(result, top_png)

    payload = json.loads(report_json.read_text(encoding="utf-8"))

    if "summary" not in payload:
        payload["summary"] = build_summary(result)

    if "top_pairs_overall" not in payload:
        payload["top_pairs_overall"] = _compute_overall_pairs(
            payload.get("files", result.files),
            payload.get("similarity_matrix", result.similarity_matrix),
            k=10,
        )

    _write_site(site_dir, report_md, report_json, payload=payload)

    print(f"Generated: {report_json}")
    print(f"Generated: {report_md}")
    if heatmap_png.exists():
        print(f"Generated: {heatmap_png}")
    if hist_png.exists():
        print(f"Generated: {hist_png}")
    if top_png.exists():
        print(f"Generated: {top_png}")
    print(f"Generated site: {site_dir / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
