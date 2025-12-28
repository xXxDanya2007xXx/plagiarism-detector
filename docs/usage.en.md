# Usage

## 1) Analyze a folder of submissions

```bash
python -m plagiarism_detector --input uploads --out reports --threshold 0.75
```

Outputs in `reports/`:
- `report.json`
- `report.md`
- `heatmap.png`

## 2) Filter formats and recursion

Specify formats:

```bash
python -m plagiarism_detector --input uploads --out reports --threshold 0.75 --exts txt,pdf,docx
```

Disable recursive scan:

```bash
python -m plagiarism_detector --input uploads --out reports --threshold 0.75 --no-recursive
```

## 3) Demo with the sample dataset

```bash
python -m plagiarism_detector --input data/sample --out reports --threshold 0.75
```

## 4) Generate a static report page

```bash
python scripts/generate_site.py --input data/sample --out reports --site site --threshold 0.75
```

`site/` contains:
- `index.html`
- `report.json`, `report.md`, `heatmap.png` (copied next to the HTML)

This makes GitHub Pages deployment straightforward.

## 5) Automation via GitHub Actions

The **Generate Report** workflow supports:
- scheduled runs (`schedule`)
- manual runs (`workflow_dispatch`)
- auto-runs on changes under `uploads/**` (via `push` + `paths`)

Triggers reference:  
https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs

## Docker

Build:
```bash
docker build -t plagiarism-detector .
```

Run:
```bash
docker run --rm \
  -v "$PWD/uploads:/app/uploads" \
  -v "$PWD/reports:/app/reports" \
  plagiarism-detector --input uploads --out reports --threshold 0.75
```
