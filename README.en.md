🇺🇸 [English](README.en.md) • 🇷🇺 [Русский](README.md)

# Plagiarism Detector

![CI](https://github.com/xXxDanya2007xXx/plagiarism-detector/actions/workflows/ci.yml/badge.svg)
![Report](https://github.com/xXxDanya2007xXx/plagiarism-detector/actions/workflows/report.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Plagiarism Detector** is a text similarity tool for student submissions.  
It builds a similarity matrix across a folder of files and highlights pairs worth manual review.

> Note: the tool measures **similarity**, not “proof of plagiarism”. Use it as a screening step.

---

## Features

- Folder-based ingestion with supported formats:
  - ✅ `.txt`
  - ✅ `.pdf`
  - ✅ `.docx`
- Similarity signals and final score (see [docs/methods.en.md](docs/methods.en.md)):
  - TF‑IDF cosine similarity
  - SequenceMatcher ratio
  - N‑gram Jaccard similarity
  - LCS similarity (token-based)
- Reports:
  - `reports/report.json` — detailed machine-readable report (includes summary)
  - `reports/report.md` — human-friendly report
  - `reports/heatmap.png` — heatmap visualization
- Static report page generation:
  - `site/index.html` + copies of `report.json`, `report.md`, `heatmap.png` (for GitHub Pages)

---

## Quick start

### Install (Linux/macOS)
```bash
git clone https://github.com/xXxDanya2007xXx/plagiarism-detector.git
cd plagiarism-detector

python3 -m venv .venv
. .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

### Run analysis
```bash
python -m plagiarism_detector --input uploads --out reports --threshold 0.75
```

Outputs: `reports/report.json`, `reports/report.md`, `reports/heatmap.png`.

---

## Docker

You can run the project in a container (this repo includes a `Dockerfile`).

### Build
```bash
docker build -t plagiarism-detector .
```

### Run (mount input/output folders)
```bash
docker run --rm \
  -v "$PWD/uploads:/app/uploads" \
  -v "$PWD/reports:/app/reports" \
  plagiarism-detector --input uploads --out reports --threshold 0.75
```

### Linux: avoid root-owned output files
If you run Docker via `sudo`, output files may be owned by `root`. Run with your UID/GID:

```bash
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD/uploads:/app/uploads" \
  -v "$PWD/reports:/app/reports" \
  plagiarism-detector --input uploads --out reports --threshold 0.75
```

### Cleanup
- Remove the image:
```bash
docker rmi plagiarism-detector
```
- Remove unused layers/containers/cache:
```bash
docker system prune
```

---

## Demo (sample dataset)

```bash
python -m plagiarism_detector --input data/sample --out reports --threshold 0.75
python scripts/generate_site.py --input data/sample --out reports --site site --threshold 0.75
```

---

## Why both `reports/` and `site/` exist

- `reports/` contains raw analysis artifacts (JSON/MD/PNG).
- `site/` contains a self-contained static page (`index.html`) plus copies of the artifacts next to it, so:
  - you can open `site/index.html` locally,
  - GitHub Pages can publish it as a static site with no external links.

Both folders are generated and typically ignored by git.

---

## CLI

```bash
python -m plagiarism_detector --help
```

Common arguments:
- `--input` — input folder
- `--out` — output folder
- `--threshold` — suspiciousness threshold (0..1)
- `--exts` — comma-separated extensions (e.g. `txt,pdf,docx`)
- `--no-recursive` — disable recursive scan
- `--no-plot` — disable `heatmap.png` (if supported by your CLI version)

---

## GitHub Actions (CI/CD)

GitHub Actions docs: https://docs.github.com/en/actions

- **CI** (`ci.yml`) runs on push/PR:
  - `black`, `flake8`, `pytest` (and `pylint` if enabled)

- **Generate Report** (`report.yml`) runs:
  - on schedule (`schedule`)
  - manually (`workflow_dispatch`)
  - on changes in `uploads/**` (via `push` + `paths`)

The workflow generates `reports/` and `site/`, uploads them as **Artifacts**, and can deploy `site/` to **GitHub Pages** (if enabled in repo settings).  
CI also checks that the `Dockerfile` builds successfully (`docker build`).
Workflow triggers reference: https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs  
GitHub Pages via Actions: https://docs.github.com/en/pages/getting-started-with-github-pages/using-github-pages-with-github-actions

---

## Documentation

- Methods and interpretation: [docs/methods.en.md](docs/methods.en.md)
- Usage/demo: [docs/usage.en.md](docs/usage.en.md)
- CI/CD: [docs/ci-cd.en.md](docs/ci-cd.en.md)

---

## Project structure

<!-- STRUCTURE_START -->
<!-- STRUCTURE_END -->

---

## License

MIT License — see [LICENSE](LICENSE).

---

<sub>Course project for “Information Technologies and Services”.</sub>
