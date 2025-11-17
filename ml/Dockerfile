FROM python:3.10-slim-buster

WORKDIR /ml

RUN pip install uv

COPY pyproject.toml uv.lock /ml/

RUN uv sync --no-dev

COPY shared/ /ml/shared/
COPY ml/src/ /ml/src/
COPY ml/app.py /ml/

ENV PYTHONPATH=/ml

CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
