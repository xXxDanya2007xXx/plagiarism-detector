from __future__ import annotations

import argparse
from pathlib import Path

import markdown as md

from plagiarism_detector.analyzer import analyze_folder
from plagiarism_detector.reporting import save_heatmap_png, save_json, save_markdown


def write_site(site_dir: Path, report_md: Path, report_json: Path, heatmap_png: Path) -> None:
    site_dir.mkdir(parents=True, exist_ok=True)

    md_text = report_md.read_text(encoding="utf-8")
    body_html = md.markdown(md_text, extensions=["tables"])

    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Plagiarism Detector Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 980px; margin: 2rem auto; padding: 0 1rem; }}
    img {{ max-width: 100%; height: auto; }}
    code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 4px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; }}
    th {{ background: #f6f6f6; }}
  </style>
</head>
<body>
  <h1>Plagiarism Detector</h1>
  <p><a href="report.json">report.json</a> • <a href="report.md">report.md</a></p>
  <h2>Heatmap</h2>
  <img src="heatmap.png" alt="Similarity heatmap"/>
  <hr/>
  {body_html}
</body>
</html>
"""
    (site_dir / "index.html").write_text(html, encoding="utf-8")
    (site_dir / "report.md").write_text(md_text, encoding="utf-8")
    (site_dir / "report.json").write_text(report_json.read_text(encoding="utf-8"), encoding="utf-8")
    (site_dir / "heatmap.png").write_bytes(heatmap_png.read_bytes())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="uploads")
    ap.add_argument("--out", default="reports")
    ap.add_argument("--site", default="site")
    ap.add_argument("--threshold", type=float, default=0.75)
    args = ap.parse_args()

    out_dir = Path(args.out)
    site_dir = Path(args.site)
    out_dir.mkdir(parents=True, exist_ok=True)

    result = analyze_folder(Path(args.input), threshold=args.threshold)

    report_json = out_dir / "report.json"
    report_md = out_dir / "report.md"
    heatmap_png = out_dir / "heatmap.png"

    save_json(result, report_json)
    save_markdown(result, report_md)
    save_heatmap_png(result, heatmap_png)

    # heatmap может не создаться при пустом наборе; тогда сайт всё равно делаем без картинки
    if heatmap_png.exists():
        write_site(site_dir, report_md, report_json, heatmap_png)
    else:
        site_dir.mkdir(parents=True, exist_ok=True)
        (site_dir / "index.html").write_text(
            "<h1>Plagiarism Detector</h1><p>No data to plot.</p>", encoding="utf-8"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
