# CI/CD

GitHub Actions docs: https://docs.github.com/en/actions

## CI (`.github/workflows/ci.yml`)

Triggers:
- `push` to `main/master`
- `pull_request`

Checks:
- `black --check` (formatting)
- `flake8` (lint/PEP8)
- `pylint` (quality gate, if enabled)
- `pytest` (unit tests)

Goal: keep the main branch green and prevent quality regressions.

## Report (`.github/workflows/report.yml`)

Triggers:
- scheduled runs (`schedule`)
- manual runs (`workflow_dispatch` with inputs)
- changes under `uploads/**` (via `push` + `paths`)

Outputs:
- uploaded as **Artifacts** (`reports/` and/or `site/`)
- optionally deployed to **GitHub Pages** (enable in Settings → Pages → Source: GitHub Actions)

Workflow triggers reference:  
https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs
