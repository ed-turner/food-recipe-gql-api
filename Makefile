


run:
	poetry run uvicorn main:app --host 0.0.0.0 --port 80

test:
	poetry run pytest -v