FROM python:3.13.2-alpine3.21

ENV LANG=C.UTF-8

RUN mkdir -p /src/app
WORKDIR /src/app

# ENV PYTHONPATH=/src/app:/src/app/source

COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]