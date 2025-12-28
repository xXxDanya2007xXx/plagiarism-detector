from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

_WORD_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9]+")


@dataclass(frozen=True)
class PreprocessConfig:
    lower: bool = True
    min_token_len: int = 2


def normalize_text(text: str, *, lower: bool = True) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower() if lower else text


def tokenize(text: str, cfg: PreprocessConfig = PreprocessConfig()) -> List[str]:
    text = normalize_text(text, lower=cfg.lower)
    tokens = _WORD_RE.findall(text)
    return [t for t in tokens if len(t) >= cfg.min_token_len]


def detokenize(tokens: List[str]) -> str:
    return " ".join(tokens)
