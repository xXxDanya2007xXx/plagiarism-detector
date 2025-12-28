# Использование

## Демонстрация на sample dataset

1) Скопировать примеры в `uploads/`:

```bash
python scripts/copy_sample_to_uploads.py
```

2) Запустить анализ:

```bash
python -m plagiarism_detector --input uploads --out reports --threshold 0.75
```

Результаты:
- `reports/report.json`
- `reports/report.md`
- `reports/heatmap.png`

## Запуск без копирования (напрямую из data/sample)

```bash
python -m plagiarism_detector --input data/sample --out reports --threshold 0.75
```

## Генерация отчёта через GitHub Actions

Workflow **Generate Report** поддерживает ручной запуск (`workflow_dispatch`).
Можно указать:
- `folder = data/sample`
- `threshold = 0.75`

После выполнения результаты будут доступны в **Artifacts** и/или на **GitHub Pages** (если включено).
