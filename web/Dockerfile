FROM python:3.10-slim-buster

WORKDIR /web

COPY /poetry.lock /web/
COPY /pyproject.toml /web/
COPY /shared /web/shared
COPY /web/src /web/src

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

ENV PYTHONPATH=/web

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
