# pull official base image.
FROM python:3.8.1-slim-buster

# set work directory.
WORKDIR /usr/src/app

# set environment variables.
ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

 # install system dependencies.
RUN apt-get update && apt-get install -y netcat

# System app dependencies.
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer.
COPY poetry.lock pyproject.toml /usr/src/app/

# Project initialization.
RUN poetry config virtualenvs.create false \
  && poetry install \
  $(if [ "$YOUR_ENV" = "production" ]; then echo "--no-dev"; fi) \
  --no-interaction --no-ansi


# copy project.
COPY . /usr/src/app/

# run entrypoint.sh.
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
