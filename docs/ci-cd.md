# CI/CD

## CI workflow (ci.yml)
Runs on every push / pull request:
- black --check
- flake8
- pylint (quality gate)
- pytest

Goal: keep main branch always green and enforce code quality.

## Report workflow (report.yml)
Runs:
- on schedule (cron)
- manually (workflow_dispatch with parameters)
- on push to main when uploads/**, src/**, scripts/** change

Produces:
- reports/ (json + md + png)
- site/ (static html report)

Publishes:
- artifacts in GitHub Actions
- GitHub Pages (via deploy-pages)
