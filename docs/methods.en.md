# Similarity methods and interpretation

The project computes **text similarity** between submissions to help identify pairs worth manual review.
Similarity ≠ proof of plagiarism.

## Pipeline

1. Read documents from a folder (`.txt/.pdf/.docx`).
2. Normalize and tokenize.
3. Compute a similarity matrix.
4. Generate reports (JSON/Markdown/PNG) and a static HTML page.

## Signals

### TF‑IDF cosine similarity
Build TF‑IDF representations (token-based) and compute cosine similarity.

### SequenceMatcher ratio
Based on `difflib.SequenceMatcher`. Good for long shared fragments.

### N‑gram Jaccard similarity
Build word n‑grams and compute:
`J(A,B) = |A ∩ B| / |A ∪ B|`.

### LCS similarity
Compute token-based LCS and normalize:
`2*LCS(a,b)/(len(a)+len(b))`.

## Final score

The final score is a weighted combination of signals. Weights/parameters are stored in `report.json -> config`
to keep runs reproducible and transparent.

## Interpreting the output

- `top_pairs` — pairs **above** the threshold
- `top_pairs_overall` — most similar pairs **overall**, even if below threshold
- `summary` — aggregate stats across all pairs (max/mean/median, pairs ≥ threshold)

## Limitations

- Templates, shared task statements, and valid quotes can increase similarity.
- Very short texts are harder to compare reliably.
- Use this tool as a screening step and review flagged pairs manually.
