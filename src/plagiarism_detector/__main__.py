from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze_folder, save_result_json


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="plagiarism_detector")
    p.add_argument("--input", default="uploads", help="Folder with submissions (.txt)")
    p.add_argument("--out", default="reports", help="Output folder")
    p.add_argument("--threshold", type=float, default=0.75, help="Suspicion threshold 0..1")
    return p


def main() -> int:
    args = build_parser().parse_args()

    result = analyze_folder(Path(args.input), threshold=args.threshold)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / "report.json"
    save_result_json(result, out_json)

    print(f"Files: {len(result.files)}")
    print(f"Saved: {out_json}")
    if result.top_pairs:
        print("Top pairs:")
        for p in result.top_pairs[:5]:
            print(f"- {p['a']} vs {p['b']}: {p['score']:.3f}")
    else:
        print("Top pairs: none (folder empty or below threshold)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
