# CI/CD

Документация GitHub Actions: https://docs.github.com/en/actions

## CI (`.github/workflows/ci.yml`)

Запускается на:
- `push` в `main/master`
- `pull_request`

Проверки:
- `black --check` (форматирование)
- `flake8` (PEP8/линт)
- `pylint` (качество кода, если включено)
- `pytest` (юнит-тесты)

Цель: не допускать деградации качества и поддерживать “зелёную” ветку.

## Report (`.github/workflows/report.yml`)

Запускается:
- по расписанию (`schedule`)
- вручную (`workflow_dispatch` с параметрами)
- при изменениях в `uploads/**` (через `push` + `paths`)

Результаты:
- сохраняются как **Artifacts** (папки `reports/` и/или `site/`)
- при необходимости деплоятся на **GitHub Pages** (включается в Settings → Pages → Source: GitHub Actions)

Документация про триггеры workflow:  
https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs
