FROM python:3.8

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

COPY gql gql
COPY models models
COPY settings.py .
COPY app.py .

ENV PORT=80

CMD ["uvicorn", "app:create_app", "--host", "0.0.0.0", "--port","80"]



