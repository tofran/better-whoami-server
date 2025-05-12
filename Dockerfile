FROM python:3.13-bookworm as builder
WORKDIR /app

COPY pyproject.toml poetry.lock poetry.toml ./

RUN curl -sSL https://install.python-poetry.org | python - && \
    /root/.local/bin/poetry install --without dev --no-interaction --no-ansi --no-directory --no-cache

FROM python:3.13-slim-bookworm as runner
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:${PATH}"

COPY --from=builder "${VIRTUAL_ENV}" "${VIRTUAL_ENV}"

COPY ./better_whoami ./better_whoami

ARG APP_VERSION=0.0.1-untagged
ENV APP_VERSION=${APP_VERSION}

EXPOSE 8000
CMD ["uvicorn", "better_whoami.app:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]
