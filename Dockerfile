FROM python:3.8

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

COPY gql .
COPY models .
COPY settings.py .
COPY app.py .

CMD ["uvicorn", "main:create_app", "--host", "0.0.0.0", "--port", "$PORT"]



