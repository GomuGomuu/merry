FROM python:3.12 as builder

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    DOCKER_BUILDKIT=1

WORKDIR /src

COPY src/config/pyproject.toml src/config/poetry.lock ./

RUN target=$POETRY_CACHE_DIR poetry install --no-root

FROM python:3.12-slim as runtime

RUN apt-get update && \
    apt-get install -y make postgresql-client procps dnsutils jq curl unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*


ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    DJANGO_SETTINGS_MODULE=config.settings \
    PYTHON_LIB_PATH=/usr/local/lib/python3.12/site-packages \
    BIN_PATH=/usr/local/bin \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

COPY --from=builder ${PYTHON_LIB_PATH} ${PYTHON_LIB_PATH}

COPY --from=builder ${BIN_PATH} ${BIN_PATH}

COPY src/ /src
COPY src/config/pyproject.toml src/config/poetry.lock ./

WORKDIR /src

RUN poetry install --without dev

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]