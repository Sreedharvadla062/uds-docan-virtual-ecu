"""Makefile-like commands for project management"""

.PHONY: help install dev test lint format clean docs

help:
	@echo "UDS DoCAN Virtual ECU - Project Commands"
	@echo "========================================="
	@echo "make install    - Install dependencies"
	@echo "make dev        - Install dev dependencies"
	@echo "make test       - Run tests with coverage"
	@echo "make lint       - Run code quality checks"
	@echo "make format     - Format code with black"
	@echo "make clean      - Clean build artifacts"
	@echo "make docs       - Generate documentation"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

lint:
	flake8 src/ tests/ --max-line-length=100
	mypy src/ --ignore-missing-imports

format:
	black src/ tests/ examples/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

docs:
	@echo "Documentation is in docs/ directory"
