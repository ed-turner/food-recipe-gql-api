#/bin/sh

poetry run uvicorn app:create_app --host 0.0.0.0 --port $PORT