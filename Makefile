.PHONY: venv install run test lint fmt fuzz perf postman ci

venv:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --port 8000

test:
	pytest -q --maxfail=1 --disable-warnings

fuzz:
	schemathesis run --checks=all http://localhost:8000/openapi.json

perf:
	locust -f perf/locustfile.py --host http://localhost:8000

postman:
	docker compose run --rm newman

ci:
	pytest -q && ruff check . && ruff format --check .