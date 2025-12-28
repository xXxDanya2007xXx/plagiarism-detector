from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="plagiarism_detector")
    p.add_argument("--input", default="uploads", help="Folder with submissions")
    p.add_argument("--out", default="reports", help="Output folder")
    p.add_argument("--threshold", type=float, default=0.75, help="Suspicion threshold 0..1")
    p.add_argument("--no-plot", action="store_true", help="Disable plots")
    return p


def main() -> int:
    p = build_parser()
    _ = p.parse_args()
    # MVP will be implemented in Iteration 1
    print("plagiarism_detector: skeleton OK (analysis not implemented yet)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
