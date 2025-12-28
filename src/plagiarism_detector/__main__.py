from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze_folder
from .reporting import save_heatmap_png, save_json, save_markdown


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="plagiarism_detector")
    p.add_argument("--input", default="uploads", help="Folder with submissions (.txt)")
    p.add_argument("--out", default="reports", help="Output folder")
    p.add_argument("--threshold", type=float, default=0.75, help="Suspicion threshold 0..1")
    p.add_argument("--no-plot", action="store_true", help="Disable heatmap PNG")
    return p


def main() -> int:
    args = build_parser().parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    result = analyze_folder(Path(args.input), threshold=args.threshold)

    save_json(result, out_dir / "report.json")
    save_markdown(result, out_dir / "report.md")
    if not args.no_plot:
        save_heatmap_png(result, out_dir / "heatmap.png")

    print(f"Files: {len(result.files)}")
    print(f"Saved: {out_dir / 'report.json'}")
    print(f"Saved: {out_dir / 'report.md'}")
    if not args.no_plot:
        print(f"Saved: {out_dir / 'heatmap.png'}")

    if result.top_pairs:
        print("Top pairs:")
        for p in result.top_pairs[:5]:
            print(f"- {p['a']} vs {p['b']}: {p['score']:.3f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
