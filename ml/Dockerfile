FROM python:3.10-slim-buster

WORKDIR /ml/

RUN pip install poetry

COPY poetry.lock pyproject.toml /ml/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY /shared /ml/shared

COPY /ml/src /ml/src
COPY /ml/app.py /ml/

ENV PYTHONPATH=/ml

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]