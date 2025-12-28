# CI/CD

GitHub Actions docs: https://docs.github.com/en/actions

## CI (`.github/workflows/ci.yml`)

Триггеры:
- `push` в `main/master`
- `pull_request`

Проверки:
- `black --check`
- `flake8`
- `pytest` (и `pylint`, если включён)

## Report (`.github/workflows/report.yml`)

Триггеры:
- `schedule` (cron)
- `workflow_dispatch`
- `push` при изменениях в `uploads/**` (через `paths`)

Действия:
- генерация `reports/` и `site/`
- загрузка **Artifacts**
- (опционально) деплой `site/` на GitHub Pages

Триггеры workflow:  
https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs

GitHub Pages via Actions:  
https://docs.github.com/en/pages/getting-started-with-github-pages/using-github-pages-with-github-actions
