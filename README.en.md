🇷🇺 [Русский](README.md) • 🇺🇸 [English](README.en.md)

# 🔎📄 Plagiarism Detector
**Plagiarism Detector** - a tool for detecting 🤥plagiarism in student 📄papers using text analysis methods and 🤖artificial intelligence technology.
✨ *Helps teachers quickly analyze the originality of papers, identify dishonest students, and maintain academic integrity.*

## 🌈 Features
- 📄 **Multi-format support**: Supports text files, DOCX, and PDF formats
- 🤓 **Smart comparison**: Multiple similarity analysis methods (...) <!-- TODO: add description -->
- 📊 **Results visualization**: Similarity matrices and detailed reports
- 🤖 **Automation**: Script runs automatically via [GitHub Actions](https://github.com/features/actions) on a schedule
- 📝 **Report generation**: Generation of detailed reports in `Markdown` and `JSON` formats

## 🎯 TODO
- [ ] Implement basic text file parsing
- [ ] Add PDF and DOCX format support
- [ ] Implement text comparison algorithms
- [ ] Create a results visualization system
- [ ] Set up automated testing
- [ ] Complete the project

## 🗃️ Project Structure
<!-- STRUCTURE_START -->
```text
.
├── .flake8
├── .github
│   └── workflows
│       ├── ci.yml
│       └── readme-tree.yml
├── .gitignore
├── LICENSE
├── README.en.md
├── README.md
├── data
│   └── sample
│       └── .gitkeep
├── docs
│   └── methods.md
├── pyproject.toml
├── requirements.txt
├── scripts
│   └── .gitkeep
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

## ⚙️🛠️ Technologies
- [**<img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="18"/> Python 3.10+**](https://www.python.org/): Main development language
- [**<img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/GitHub_Invertocat_Logo.svg" width="18"/> GitHub Actions**](https://github.com/features/actions): CI/CD automation

## 🚀 Installation and Running
### <img src="https://upload.wikimedia.org/wikipedia/commons/3/35/Tux.svg" width="24"/> Linux/ <img src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg" width="24"/> macOS
```
# Clone the repository
git clone https://github.com/xXxDanya2007xXx/plagiarism-detector.git
cd plagiarism-detector

# Install and activate virtual environment
python3 -m venv .venv
. .venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Run
...
```

### <img src="https://upload.wikimedia.org/wikipedia/commons/8/87/Windows_logo_-_2021.svg" width="24"/> Windows
```
:: Clone the repository
git clone https://github.com/xXxDanya2007xXx/plagiarism-detector.git
cd plagiarism-detector

:: Install and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt

:: Run
...
```

> [!TIP]
> Use the `deactivate` command to exit the virtual environment

---

<p align="center"> 
    <sub>* Project completed as part of the «Information Technologies and Services» course<br></sub> 
</p>
