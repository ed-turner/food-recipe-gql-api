

install.dev:
	poetry install

install.prod:
	poetry install --no-dev -E production

run:
	uvicorn main:app --host 0.0.0.0 --port 80