# CI/CD

GitHub Actions docs: https://docs.github.com/en/actions

## CI (`.github/workflows/ci.yml`)

Triggers:
- `push` to `main/master`
- `pull_request`

Checks:
- `black --check`
- `flake8`
- `pytest` (and `pylint` if enabled)

## Report (`.github/workflows/report.yml`)

Triggers:
- `schedule` (cron)
- `workflow_dispatch`
- `push` on changes under `uploads/**` (via `paths`)

Actions:
- generate `reports/` and `site/`
- upload **Artifacts**
- (optional) deploy `site/` to GitHub Pages

Workflow triggers reference:  
https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs

GitHub Pages via Actions:  
https://docs.github.com/en/pages/getting-started-with-github-pages/using-github-pages-with-github-actions
