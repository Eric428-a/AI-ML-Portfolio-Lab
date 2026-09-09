# Makefile

install:
	pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	ruff check app tests scripts

format:
	black app tests scripts

format-check:
	black --check app tests scripts

security:
	pip-audit

check:
	ruff check app tests scripts
	black --check app tests scripts
	pytest

docker-build:
	docker build -t pdf-question-answering-bot .

docker-up:
	docker compose up --build

docker-down:
	docker compose down

rebuild-index:
	python scripts/rebuild_index.py

help:
	@echo "Available commands:"
	@echo "  install        Install dependencies"
	@echo "  dev            Start development server"
	@echo "  run            Start production server"
	@echo "  test           Run tests"
	@echo "  lint           Run Ruff"
	@echo "  format         Format Python code"
	@echo "  format-check   Check Black formatting"
	@echo "  security       Run pip-audit"
	@echo "  check          Run lint, format check and tests"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-up      Start Docker Compose"
	@echo "  docker-down    Stop Docker Compose"
	@echo "  rebuild-index  Rebuild vector index"