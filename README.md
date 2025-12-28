🇺🇸 [English](README.en.md) • 🇷🇺 [Русский](README.md)

# Plagiarism Detector

![CI](https://github.com/xXxDanya2007xXx/plagiarism-detector/actions/workflows/ci.yml/badge.svg)
![Report](https://github.com/xXxDanya2007xXx/plagiarism-detector/actions/workflows/report.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Plagiarism Detector** — инструмент для поиска текстовых совпадений в студенческих работах.  
Он строит матрицу схожести по набору работ и помогает преподавателю быстро найти *подозрительно похожие* пары для ручной проверки.

> Важно: инструмент измеряет **схожесть текста**, а не “доказывает плагиат”. Используйте как этап предварительного скрининга.

---

## Возможности

- Анализ набора работ из папки (`uploads/`) и расчёт **матрицы схожести**
- Несколько метрик сходства (см. [docs/methods.md](docs/methods.md))
- Отчёты:
  - `reports/report.json` — машинно-читаемый результат
  - `reports/report.md` — краткий отчёт для человека
  - `reports/heatmap.png` — визуализация матрицы
- Автоматизация через GitHub Actions:
  - CI: стиль кода + тесты
  - Отчёты по расписанию/вручную/при изменении `uploads/` (см. [docs/ci-cd.md](docs/ci-cd.md))

### Форматы файлов
- ✅ Сейчас: `.txt`
- ⏳ В планах: `.pdf`, `.docx` (см. Roadmap)

---

## Быстрый старт

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

> Чтобы выйти из виртуального окружения: `deactivate`

---

## Использование

### Пример
1) Положите `.txt` файлы в `uploads/` (например, `uploads/work1.txt`, `uploads/work2.txt`).
2) Запустите анализ:

```bash
python -m plagiarism_detector --input uploads --out reports --threshold 0.75
```

Результаты появятся в `reports/`:
- `report.json`
- `report.md`
- `heatmap.png`

### Параметры CLI
- `--input` — папка с работами (по умолчанию `uploads`)
- `--out` — папка для отчётов (по умолчанию `reports`)
- `--threshold` — порог “подозрительности” (0..1, по умолчанию `0.75`)
- `--no-plot` — отключить генерацию `heatmap.png` (если поддерживается в вашей версии CLI)

---

## GitHub Actions (CI/CD)

Проект использует GitHub Actions: https://docs.github.com/en/actions

- **CI workflow** (`ci.yml`) запускается на каждый push/PR и выполняет:
  - форматирование/стиль (`black`, `flake8`)
  - качество кода (`pylint`, если включён)
  - тесты (`pytest`)

- **Report workflow** (`report.yml`) запускается:
  - по расписанию (`schedule`)
  - вручную (`workflow_dispatch` с параметрами)
  - при изменениях в `uploads/**` (через `push` + `paths`)
  - сохраняет результаты как **Artifacts**, а также может публиковать отчёт на **GitHub Pages** (если включено в настройках репозитория)

Подробности: [docs/ci-cd.md](docs/ci-cd.md)

---

## Документация

- Метрики и интерпретация результатов: [docs/methods.md](docs/methods.md)
- CI/CD и автоматизация: [docs/ci-cd.md](docs/ci-cd.md)
- Использование и демо-датасет: [docs/usage.md](docs/usage.md)

---

## Разработка

### Запуск проверок локально
```bash
pip install -r requirements.txt
pip install -e .

pytest -q
flake8 src tests scripts
black --check src tests scripts
```

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
│   ├── test_reporting.py
│   ├── test_sample_dataset.py
│   ├── test_similarity.py
│   ├── test_similarity_tfidf.py
│   └── test_smoke.py
└── uploads
    └── .gitkeep
```
<!-- STRUCTURE_END -->

---

## Roadmap

- [ ] Поддержка `.pdf` и `.docx`
- [ ] Дополнительные метрики (например, LCS / шинглы) и “объяснения” по скору
- [ ] Улучшение визуализаций и отчётов
- [ ] Расширение набора тестов и покрытие edge-case’ов

---

## Ограничения и этичное использование

- Высокая схожесть может быть вызвана шаблонами, формулировкой задания, корректными цитатами.
- Для коротких текстов метрики менее стабильны.
- Рекомендуется использовать результат как *сигнал*, а затем проверять пары вручную.

---

## Лицензия

MIT License — см. файл [LICENSE](LICENSE).

---

<sub>Проект выполнен в рамках курса «Информационные Технологии и Сервисы».</sub>
