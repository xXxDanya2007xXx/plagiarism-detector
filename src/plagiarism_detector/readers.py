from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Document:
    name: str
    text: str
    path: Path


def read_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_folder(folder: Path, *, exts: tuple[str, ...] = (".txt",)) -> List[Document]:
    folder = Path(folder)
    if not folder.exists():
        return []

    paths = sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in exts)
    return [Document(name=p.name, text=read_txt(p), path=p) for p in paths]
