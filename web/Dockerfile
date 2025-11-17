FROM python:3.10-slim-buster

WORKDIR /web

COPY /shared /web/shared
COPY /web/src /web/src

# Установить uv (через pipx — идеальный вариант)
RUN pip install uv

# Копируем pyproject.toml и uv.lock (если есть)
COPY pyproject.toml uv.lock /web/

# Устанавливаем зависимости в системную среду (без виртуальных окружений)
RUN uv sync --no-dev

ENV PYTHONPATH=/web

CMD ["uv", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
