# Использование

## 1) Анализ папки с работами

```bash
python -m plagiarism_detector --input uploads --out reports --threshold 0.75
```

Результаты появятся в `reports/`:
- `report.json`
- `report.md`
- `heatmap.png`

## 2) Фильтрация форматов и обход подпапок

Указать форматы (через запятую):

```bash
python -m plagiarism_detector --input uploads --out reports --threshold 0.75 --exts txt,pdf,docx
```

Отключить рекурсивный обход:

```bash
python -m plagiarism_detector --input uploads --out reports --threshold 0.75 --no-recursive
```

## 3) Демо на sample dataset

```bash
python -m plagiarism_detector --input data/sample --out reports --threshold 0.75
```

## 4) Генерация статической страницы отчёта

```bash
python scripts/generate_site.py --input data/sample --out reports --site site --threshold 0.75
```

Папка `site/` содержит:
- `index.html`
- `report.json`, `report.md`, `heatmap.png` (копии рядом с HTML)

Это сделано специально для удобной публикации на GitHub Pages.

## 5) Автоматическая генерация через GitHub Actions

Workflow **Generate Report** поддерживает:
- расписание (`schedule`)
- ручной запуск (`workflow_dispatch`)
- автозапуск при изменениях в `uploads/**` (через `push` + `paths`)

Документация по триггерам:  
https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs

## Docker

Сборка:
```bash
docker build -t plagiarism-detector .
```

Запуск:
```bash
docker run --rm \
  -v "$PWD/uploads:/app/uploads" \
  -v "$PWD/reports:/app/reports" \
  plagiarism-detector --input uploads --out reports --threshold 0.75
```
