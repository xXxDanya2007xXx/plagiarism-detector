# Similarity methods and interpretation

This project computes **text similarity** between submissions to help identify pairs worth manual review.
Similarity ≠ proof of plagiarism.

## Pipeline

1. Read files from a folder (currently `.txt`).
2. Normalize/tokenize text.
3. Compute pairwise similarity matrix.
4. Generate reports: JSON, Markdown, and a PNG heatmap.

## Similarity signals

The exact set can evolve; the current configuration is saved in `report.json` under `config`.

### TF‑IDF cosine similarity
Build TF‑IDF vectors and compute cosine similarity.
- Strong baseline for lexical overlap
- Reasonably robust to noise

### SequenceMatcher ratio
Based on `difflib.SequenceMatcher`.
- Good for near-copy cases and long shared fragments
- Sensitive to reordering

### N‑gram Jaccard similarity
Build word n‑grams and compute:
`J(A,B) = |A ∩ B| / |A ∪ B|`
- Useful for partial copying and shared phrasing

## Final score

The final score is typically a weighted combination of multiple signals.
Weights/parameters are stored in `report.json -> config` for transparency and reproducibility.

## Threshold

- Default: `0.75`
- Increase to reduce false positives.
- Decrease to catch more suspicious pairs (more manual review needed).

## Limitations

- Templates, shared task statements, and valid quotations can increase similarity.
- Very short texts are harder to compare reliably.
- Without semantic models, paraphrases may not be captured well.
