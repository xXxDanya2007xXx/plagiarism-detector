from __future__ import annotations

import shutil
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    src_dir = root / "data" / "sample"
    dst_dir = root / "uploads"
    dst_dir.mkdir(parents=True, exist_ok=True)

    for p in src_dir.glob("*.txt"):
        shutil.copyfile(p, dst_dir / p.name)

    print(f"Copied {len(list(src_dir.glob('*.txt')))} files to {dst_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
