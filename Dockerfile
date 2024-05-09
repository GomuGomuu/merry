FROM python:3.12.3

ENV PYHTONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install --yes libmagic-dev curl
RUN mkdir -p /usr/app
WORKDIR /usr/app
ADD src/config/pyproject.toml ./config/pyproject.toml
RUN pip install poetry
RUN poetry install -C ./config/
COPY . /usr/app


ENTRYPOINT ["sh", "docker-entrypoint.sh"]