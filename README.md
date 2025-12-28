🇺🇸 [English](README.en.md) • 🇷🇺 [Русский](README.md)

# 🔎📄 Plagiarism Detector
**Plagiarism Detector** - инструмент для выявления 🤥плагиата в студенческих 📄работах с использованием методов анализа текста и технологии 🤖искусственного интеллекта.  
✨ *Помогает преподавателям быстро анализировать оригинальность работ, выявлять недобросовестных студентов и поддерживать академическую честность.*

## 🌈 Функционал
- 📄 **Мультиформатная поддержка**: Работа с текстовыми файлами, DOCX и PDF
- 🤓 **Умное сравнение**: Несколько методов анализа сходства (...) <!-- TODO: добавить описание -->
- 📊 **Визуализация результатов**: Матрицы схожести и детальные отчеты
- 🤖 **Автоматизация**: Скрипт запускается автоматически через [GitHub Actions](https://github.com/features/actions) по расписанию 
- 📝 **Генерация отчетов**: Создание подробных отчетов в формате `Markdown` и `JSON`

## 🎯 TODO
- [ ] Реализовать базовый парсинг текстовых файлов
- [ ] Добавить поддержку PDF и DOCX форматов
- [ ] Реализовать алгоритмы сравнения текстов
- [ ] Создать систему визуализации результатов
- [ ] Настроить автоматизированное тестирование
- [ ] Завершить проект

## 🗃️ Структура проекта
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
│       └── .gitkeep
├── docs
│   ├── ci-cd.md
│   └── methods.md
├── pyproject.toml
├── requirements.txt
├── scripts
│   ├── .gitkeep
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
│   ├── test_similarity.py
│   ├── test_similarity_tfidf.py
│   └── test_smoke.py
└── uploads
    └── .gitkeep
```
<!-- STRUCTURE_END -->

## ⚙️🛠️ Технологии
- [**<img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="18"/> Python 3.10+**](https://www.python.org/): Основной язык разработки
- [**<img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/GitHub_Invertocat_Logo.svg" width="18"/> GitHub Actions**](https://github.com/features/actions): CI/CD автоматизация

## 🚀 Установка и запуск
### <img src="https://upload.wikimedia.org/wikipedia/commons/3/35/Tux.svg" width="24"/> Linux/ <img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" width="24"/> macOS
```sh
# Клонируем репозиторий
git clone https://github.com/xXxDanya2007xXx/plagiarism-detector.git
cd plagiarism-detector

# Устанавливаем и активируем виртуальное окружение
python3 -m venv .venv
. .venv/bin/activate

# Устанавливаем зависимости
pip3 install -r requirements.txt

# Запускаем
...
```

### <img src="https://upload.wikimedia.org/wikipedia/commons/8/87/Windows_logo_-_2021.svg" width="24"/> Windows
```cmd
:: Клонируем репозиторий
git clone https://github.com/xXxDanya2007xXx/plagiarism-detector.git
cd plagiarism-detector

:: Устанавливаем и активируем виртуальное окружение
python -m venv .venv
.venv\Scripts\activate

:: Устанавливаем зависимости
pip install -r requirements.txt

:: Запускаем
...
```

> [!TIP]
> Для выхода из виртуального окружения используйте команду `deactivate`

---

<p align="center">
    <sub>* Проект выполнен в рамках курса «Информационные Технологии и Cервисы»<br></sub>
</p>

