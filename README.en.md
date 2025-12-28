🇺🇸 [English](README.en.md) • 🇷🇺 [Русский](README.md)

# Plagiarism Detector

![CI](https://github.com/xXxDanya2007xXx/plagiarism-detector/actions/workflows/ci.yml/badge.svg)
![Report](https://github.com/xXxDanya2007xXx/plagiarism-detector/actions/workflows/report.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Plagiarism Detector** is a text similarity tool for student submissions.  
It builds a pairwise similarity matrix across a folder of files and highlights *suspiciously similar* pairs for manual review.

> Note: this tool measures **similarity**, not “proof of plagiarism”. Use it as a screening step.

---

## Features

- Analyze a folder of submissions (`uploads/`) and compute a **similarity matrix**
- Multiple similarity signals (see [docs/methods.en.md](docs/methods.en.md))
- Outputs:
  - `reports/report.json` — machine-readable results
  - `reports/report.md` — human-friendly report
  - `reports/heatmap.png` — similarity heatmap
- GitHub Actions automation:
  - CI: style checks + tests
  - Scheduled/manual/on-change reports (see [docs/ci-cd.en.md](docs/ci-cd.en.md))

### Supported formats
- ✅ Current: `.txt`
- ⏳ Planned: `.pdf`, `.docx` (see Roadmap)

---

## Quick start

### Linux / macOS
```bash
git clone https://github.com/xXxDanya2007xXx/plagiarism-detector.git
cd plagiarism-detector

python3 -m venv .venv
. .venv/bin/activate

pip install -r requirements.txt
pip install -e .

python -m plagiarism_detector --input uploads --out reports --threshold 0.75
```

### Windows (PowerShell)
```powershell
git clone https://github.com/xXxDanya2007xXx/plagiarism-detector.git
cd plagiarism-detector

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
pip install -e .

python -m plagiarism_detector --input uploads --out reports --threshold 0.75
```

> To exit the venv: `deactivate`

---

## Usage

1) Put `.txt` files into `uploads/`.
2) Run:

```bash
python -m plagiarism_detector --input uploads --out reports --threshold 0.75
```

Results will be saved to `reports/`:
- `report.json`
- `report.md`
- `heatmap.png`

### CLI arguments
- `--input` — input folder (default: `uploads`)
- `--out` — output folder (default: `reports`)
- `--threshold` — suspiciousness threshold (0..1, default: `0.75`)
- `--no-plot` — disable heatmap generation (if supported by your CLI version)

---

## GitHub Actions (CI/CD)

GitHub Actions docs: https://docs.github.com/en/actions

- **CI workflow** (`ci.yml`) runs on every push/PR and executes:
  - formatting/style checks (`black`, `flake8`)
  - code quality gate (`pylint`, if enabled)
  - unit tests (`pytest`)

- **Report workflow** (`report.yml`) runs:
  - on schedule (`schedule`)
  - manually (`workflow_dispatch` with inputs)
  - on changes in `uploads/**` (via `push` + `paths`)
  - uploads results as **Artifacts** and can publish the latest report to **GitHub Pages** (if enabled in repo settings)

Details: [docs/ci-cd.en.md](docs/ci-cd.en.md)

---

## Documentation

- Similarity methods and interpretation: [docs/methods.en.md](docs/methods.en.md)
- CI/CD automation: [docs/ci-cd.en.md](docs/ci-cd.en.md)

---

## Development

```bash
pip install -r requirements.txt
pip install -e .

pytest -q
flake8 src tests scripts
black --check src tests scripts
```

---

## Project structure

<!-- STRUCTURE_START -->
```text
# This block is auto-updated by CI (readme-tree workflow), do not edit manually.
```
<!-- STRUCTURE_END -->

---

## Roadmap

- [ ] Add `.pdf` and `.docx` support
- [ ] Add more similarity methods and per-score explanations
- [ ] Improve reports and visualizations
- [ ] Expand tests and edge-case coverage

---

## Limitations / ethical use

- Similarity may be caused by templates, shared task statements, or valid quotations.
- Very short texts are harder to compare reliably.
- Use the tool as a screening signal and review flagged pairs manually.

---

## License

MIT License — see [LICENSE](LICENSE).

---

<sub>Course project for “Information Technologies and Services”.</sub>
