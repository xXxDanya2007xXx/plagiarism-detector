from __future__ import annotations

import argparse
import inspect
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import markdown as md

from plagiarism_detector.analyzer import analyze_folder
from plagiarism_detector.reporting import (
    build_summary,
    save_heatmap_png,
    save_json,
    save_markdown,
    top_pairs_overall,
)


def _html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _format_cell(v: Any) -> str:
    if isinstance(v, float):
        return f"{v:.4f}"
    return str(v)


def _pairs_table_html(pairs: List[Dict[str, Any]]) -> str:
    if not pairs:
        return "<p><em>No pairs to show.</em></p>"

    preferred = ["a", "b", "score", "tfidf", "sequence", "ngram", "lcs"]
    present = set()
    for p in pairs:
        present.update(p.keys())

    cols = [c for c in preferred if c in present] + sorted(
        [k for k in present if k not in preferred]
    )

    head = "".join(f"<th>{_html_escape(c)}</th>" for c in cols)

    rows: List[str] = []
    for p in pairs:
        tds: List[str] = []
        for c in cols:
            cell = _format_cell(p.get(c, ""))
            tds.append(f"<td>{_html_escape(cell)}</td>")
        rows.append("<tr>" + "".join(tds) + "</tr>")

    return f"""
<table>
  <thead><tr>{head}</tr></thead>
  <tbody>
    {''.join(rows)}
  </tbody>
</table>
"""


def _matrix_table_html(files: Sequence[str], matrix: Sequence[Sequence[float]]) -> str:
    n = len(files)
    if n == 0 or n != len(matrix):
        return "<p><em>No matrix available.</em></p>"

    # Header row
    thead = "<th></th>" + "".join(f"<th>{_html_escape(name)}</th>" for name in files)

    # Body rows
    body_rows: List[str] = []
    for i in range(n):
        row = [f"<th>{_html_escape(files[i])}</th>"]
        for j in range(n):
            v = float(matrix[i][j])
            row.append(f"<td style='text-align:right'>{v:.3f}</td>")
        body_rows.append("<tr>" + "".join(row) + "</tr>")

    return f"""
<div style="overflow:auto; border:1px solid #eee; border-radius:10px;">
<table style="margin:0; min-width: 700px;">
  <thead><tr>{thead}</tr></thead>
  <tbody>
    {''.join(body_rows)}
  </tbody>
</table>
</div>
"""


def _parse_exts(value: str) -> Optional[List[str]]:
    v = value.strip()
    if not v:
        return None
    parts = [p.strip() for p in v.split(",")]
    return [p for p in parts if p]


def _write_site(
    site_dir: Path,
    report_md: Path,
    report_json: Path,
    heatmap_png: Path,
    *,
    created_at_utc: str,
    threshold: float,
    summary: Dict[str, Any],
    pairs_for_page: List[Dict[str, Any]],
    files: Sequence[str],
    matrix: Sequence[Sequence[float]],
) -> None:
    site_dir.mkdir(parents=True, exist_ok=True)

    # Copy raw artifacts for download from the page
    md_text = report_md.read_text(encoding="utf-8")
    (site_dir / "report.md").write_text(md_text, encoding="utf-8")
    (site_dir / "report.json").write_text(report_json.read_text(encoding="utf-8"), encoding="utf-8")

    heatmap_block = "<p><em>No heatmap available.</em></p>"
    if heatmap_png.exists():
        shutil.copyfile(heatmap_png, site_dir / "heatmap.png")
        heatmap_block = '<img src="heatmap.png" alt="Similarity heatmap"/>'

    # Render markdown properly (fenced code blocks + tables)
    body_html = md.markdown(md_text, extensions=["tables", "fenced_code"])

    summary_html = f"""
<div class="cards">
  <div class="card"><div class="k">Created (UTC)</div><div class="v small">{_html_escape(created_at_utc)}</div></div>
  <div class="card"><div class="k">Threshold</div><div class="v">{threshold:.2f}</div></div>
  <div class="card"><div class="k">Files</div><div class="v">{summary.get('n_files')}</div></div>
  <div class="card"><div class="k">Pairs</div><div class="v">{summary.get('n_pairs')}</div></div>
  <div class="card"><div class="k">Pairs ≥ threshold</div><div class="v">{summary.get('pairs_above_threshold')}</div></div>
  <div class="card"><div class="k">Max score</div><div class="v">{_format_cell(summary.get('max_pair_score', '-'))}</div></div>
</div>
"""

    pairs_html = _pairs_table_html(pairs_for_page)

    # Show matrix table only for small N
    matrix_html = ""
    if len(files) <= 20 and len(files) > 0:
        matrix_html = _matrix_table_html(files, matrix)
    else:
        matrix_html = "<p class='muted'><em>Matrix table is shown only when N ≤ 20 (use heatmap for larger sets).</em></p>"

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
  <p class="muted">Showing the most similar pairs (overall). If threshold-filtered list is empty, this section is still populated.</p>
  {pairs_html}

  <h2>Matrix</h2>
  {matrix_html}

  <h2>Heatmap</h2>
  {heatmap_block}

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
        help="Comma-separated extensions, e.g. 'txt,pdf,docx' (optional; used only if analyzer supports it)",
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

    # Call analyze_folder with only the parameters it supports (robust to local refactors)
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

    save_json(result, report_json)
    save_markdown(result, report_md)
    save_heatmap_png(result, heatmap_png)

    # Load JSON to reuse enriched fields (top_pairs_overall etc.), then render page.
    payload = json.loads(report_json.read_text(encoding="utf-8"))
    summary = payload.get("summary", build_summary(result))

    # Prefer threshold-filtered list; if empty, show overall top pairs
    pairs_for_page = (
        payload.get("top_pairs")
        or payload.get("top_pairs_overall")
        or top_pairs_overall(result.files, result.similarity_matrix, k=10)
    )

    _write_site(
        site_dir,
        report_md,
        report_json,
        heatmap_png,
        created_at_utc=payload.get("created_at_utc", result.created_at_utc),
        threshold=float(payload.get("threshold", result.threshold)),
        summary=summary,
        pairs_for_page=pairs_for_page,
        files=payload.get("files", result.files),
        matrix=payload.get("similarity_matrix", result.similarity_matrix),
    )

    print(f"Generated: {report_json}")
    print(f"Generated: {report_md}")
    if heatmap_png.exists():
        print(f"Generated: {heatmap_png}")
    print(f"Generated site: {site_dir / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
