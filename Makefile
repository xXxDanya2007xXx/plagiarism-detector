.PHONY: install lint test run-sample run-uploads report-site docker-build

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

lint:
	black --check src tests scripts
	flake8 src tests scripts
	pylint src/plagiarism_detector --fail-under=7.5

test:
	pytest -q

run-sample:
	python -m plagiarism_detector --input data/sample --out reports --threshold 0.75

run-uploads:
	python -m plagiarism_detector --input uploads --out reports --threshold 0.75

report-site:
	python scripts/generate_site.py --input data/sample --out reports --site site --threshold 0.75

docker-build:
	docker build -t plagiarism-detector .
