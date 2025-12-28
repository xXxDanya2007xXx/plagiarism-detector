# Usage

## Demo with the sample dataset

1) Copy sample files into `uploads/`:

```bash
python scripts/copy_sample_to_uploads.py
```

2) Run the analysis:

```bash
python -m plagiarism_detector --input uploads --out reports --threshold 0.75
```

Outputs:
- `reports/report.json`
- `reports/report.md`
- `reports/heatmap.png`

## Quick commands (Makefile)

```bash
make install
make lint
make test
make run-sample
```

## Run directly from data/sample

```bash
python -m plagiarism_detector --input data/sample --out reports --threshold 0.75
```

## Generate a report via GitHub Actions

The **Generate Report** workflow supports manual runs (`workflow_dispatch`).
You can set:
- `folder = data/sample`
- `threshold = 0.75`

Results will be available as **Artifacts** and/or on **GitHub Pages** (if enabled).
