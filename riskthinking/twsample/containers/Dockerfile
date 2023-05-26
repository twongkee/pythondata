# syntax=docker/dockerfile:1
FROM python:3.11.3-slim as twpython311
COPY . /twcode

ENV \
    POETRY_HOME=/opt/poetry \
    POETRY_VERSION=1.4.2 \
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"



RUN apt-get update \
   && apt-get install --no-install-recommends -y \
      curl \
      build-essential

RUN curl -sSL https://install.python-poetry.org | python3 -
CMD python /twcode/zap.py

