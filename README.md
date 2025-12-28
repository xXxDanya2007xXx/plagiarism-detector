🇺🇸 [English](README.en.md) • 🇷🇺 [Русский](README.md)

# Plagiarism Detector

![CI](https://github.com/xXxDanya2007xXx/plagiarism-detector/actions/workflows/ci.yml/badge.svg)
![Report](https://github.com/xXxDanya2007xXx/plagiarism-detector/actions/workflows/report.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Plagiarism Detector** — инструмент для поиска текстовых совпадений в студенческих работах.  
Он строит матрицу схожести по набору работ и выделяет пары, которые стоит проверить вручную.

> Важно: инструмент измеряет **схожесть текста**, а не “доказывает плагиат”. Используйте как этап предварительного скрининга.

---

## Возможности

- Загрузка работ из папки и поддержка форматов:
  - ✅ `.txt`
  - ✅ `.pdf`
  - ✅ `.docx`
- Метрики схожести и итоговый скор (см. [docs/methods.md](docs/methods.md)):
  - TF‑IDF cosine similarity
  - SequenceMatcher ratio
  - N‑gram Jaccard similarity
  - LCS similarity (по токенам)
- Отчёты:
  - `reports/report.json` — подробный машинно-читаемый отчёт (включая summary)
  - `reports/report.md` — отчёт для человека
  - `reports/heatmap.png` — визуализация матрицы
- Генерация статической страницы отчёта:
  - `site/index.html` + копии `report.json`, `report.md`, `heatmap.png` (для GitHub Pages)

---

## Быстрый старт

### 1) Установка (Linux/macOS)
```bash
git clone https://github.com/xXxDanya2007xXx/plagiarism-detector.git
cd plagiarism-detector

python3 -m venv .venv
. .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

### 2) Запуск анализа
```bash
python -m plagiarism_detector --input uploads --out reports --threshold 0.75
```

Результаты: `reports/report.json`, `reports/report.md`, `reports/heatmap.png`.

---

## Docker

Проект можно запускать в контейнере (в репозитории есть `Dockerfile`).

### Сборка образа
```bash
docker build -t plagiarism-detector .
```

### Запуск (монтируем папки с входом/выходом)
```bash
docker run --rm \
  -v "$PWD/uploads:/app/uploads" \
  -v "$PWD/reports:/app/reports" \
  plagiarism-detector --input uploads --out reports --threshold 0.75
```

### Linux: чтобы файлы в `reports/` создавались от вашего пользователя
Если запускаете Docker через `sudo`, файлы в `reports/` могут создаваться с владельцем `root`.
Можно запускать контейнер от текущего UID/GID:

```bash
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD/uploads:/app/uploads" \
  -v "$PWD/reports:/app/reports" \
  plagiarism-detector --input uploads --out reports --threshold 0.75
```

### Очистка (если нужно)
- Удалить образ:
```bash
docker rmi plagiarism-detector
```
- Удалить “мусор” (неиспользуемые слои/контейнеры/кэш):
```bash
docker system prune
```

---

## Демонстрация на sample dataset

```bash
python -m plagiarism_detector --input data/sample --out reports --threshold 0.75
python scripts/generate_site.py --input data/sample --out reports --site site --threshold 0.75
```

---

## Папки `reports/` и `site/` — почему обе нужны

- `reports/` содержит **выходные артефакты анализа** (JSON/MD/PNG).
- `site/` содержит **статический сайт** (`index.html`) и копии артефактов рядом, чтобы:
  - можно было открыть `site/index.html` локально,
  - GitHub Pages мог опубликовать отчёт как статический сайт без внешних ссылок.

Обе папки — генерируемые. Обычно они добавлены в `.gitignore`.

---

## CLI

```bash
python -m plagiarism_detector --help
```

Типичные аргументы:
- `--input` — папка с работами
- `--out` — папка для отчётов
- `--threshold` — порог “подозрительности” (0..1)
- `--exts` — список расширений через запятую (например: `txt,pdf,docx`)
- `--no-recursive` — не обходить подпапки
- `--no-plot` — отключить генерацию `heatmap.png` (если поддерживается вашей версией CLI)

---

## GitHub Actions (CI/CD)

Документация GitHub Actions: https://docs.github.com/en/actions

- **CI** (`ci.yml`) запускается на push/PR и выполняет:
  - `black`, `flake8`, `pytest` (и `pylint`, если включён)

- **Generate Report** (`report.yml`) запускается:
  - по расписанию (`schedule`)
  - вручную (`workflow_dispatch`)
  - при изменениях в `uploads/**` (через `push` + `paths`)

Workflow генерирует `reports/` и `site/`, загружает их как **Artifacts** и может публиковать `site/` на **GitHub Pages** (если включено в настройках репозитория).  
Также CI включает проверку, что `Dockerfile` собирается (`docker build`).
Документация по триггерам: https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs  
GitHub Pages через Actions: https://docs.github.com/en/pages/getting-started-with-github-pages/using-github-pages-with-github-actions

---

## Документация

- Метрики и интерпретация: [docs/methods.md](docs/methods.md)
- Использование/демо: [docs/usage.md](docs/usage.md)
- CI/CD: [docs/ci-cd.md](docs/ci-cd.md)

---

## Структура проекта

<!-- STRUCTURE_START -->
```text
.
├── .dockerignore
├── .flake8
├── .github
│   └── workflows
│       ├── ci.yml
│       ├── readme-tree.yml
│       └── report.yml
├── .gitignore
├── .pylintrc
├── Dockerfile
├── LICENSE
├── Makefile
├── README.en.md
├── README.md
├── data
│   └── sample
│       ├── .gitkeep
│       ├── README.md
│       ├── essay_01.txt
│       ├── essay_02_similar.txt
│       └── essay_03_unrelated.txt
├── docs
│   ├── ci-cd.en.md
│   ├── ci-cd.md
│   ├── methods.en.md
│   ├── methods.md
│   ├── usage.en.md
│   └── usage.md
├── pyproject.toml
├── requirements.txt
├── scripts
│   ├── .gitkeep
│   ├── copy_sample_to_uploads.py
│   └── generate_site.py
├── src
│   └── plagiarism_detector
│       ├── __init__.py
│       ├── __main__.py
│       ├── analyzer.py
│       ├── preprocess.py
│       ├── readers.py
│       ├── reporting.py
│       └── similarity.py
├── tests
│   ├── test_analyzer.py
│   ├── test_preprocess.py
│   ├── test_readers_formats.py
│   ├── test_reporting.py
│   ├── test_sample_dataset.py
│   ├── test_similarity.py
│   ├── test_similarity_lcs.py
│   ├── test_similarity_tfidf.py
│   ├── test_site_generation.py
│   └── test_smoke.py
└── uploads
    └── .gitkeep
```
<!-- STRUCTURE_END -->

---

## Лицензия

MIT License — см. [LICENSE](LICENSE).

---

<sub>Проект выполнен в рамках курса «Информационные Технологии и Сервисы».</sub>
