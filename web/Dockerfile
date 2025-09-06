FROM python:3.10-slim-buster

WORKDIR /web

RUN pip install poetry

COPY /poetry.lock /web/
COPY /pyproject.toml /web/

COPY /shared /web/shared

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY /web/src /web/src

ENV PYTHONPATH=/web

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
