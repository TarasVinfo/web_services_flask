###############
# python-base #
###############

# pull official base image
FROM python:3.8.1-slim-buster as python-base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/opt/poetry \
    VENV_PATH=/opt/venv \
    POETRY_VERSION=1.0.0
ENV PATH="$POETRY_PATH/bin:$VENV_PATH/bin:$PATH"


##########
# poetry #
##########
FROM python-base as poetry
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # dependencies for installing poetry
        curl \
        # dependencies for building python dependencies
        build-essential \
    \
    # install poetry - uses $POETRY_VERSION internally
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
    && mv /root/.poetry $POETRY_PATH \
    && poetry --version \
    \
    # configure poetry & make a virtualenv ahead of time since we only need one
    && python -m venv $VENV_PATH \
    && poetry config virtualenvs.create false \
    \
    # cleanup
    && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --no-ansi -vvv


#########
# FINAL #
#########

# pull official base image
FROM python-base as final

# set work directory
WORKDIR /usr/src/app

# create directory for the app user
RUN mkdir -p /home/app_user

# create the app user
RUN groupadd -r app_user && useradd -r -g app_user app_user

# create the appropriate directories
ENV HOME=/home/app_user
ENV APP_HOME=/home/app_user/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=poetry $VENV_PATH $VENV_PATH

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app_user:app_user $APP_HOME


# change to the app user
USER app_user

# run entrypoint.sh
ENTRYPOINT ["/home/app_user/web/entrypoint.sh"]
