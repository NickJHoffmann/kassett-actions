FROM python:3.9-slim as base

WORKDIR /workdir
# Update outdated setuptools version, addresses https://github.com/advisories/GHSA-r9hx-vwmv-q579
RUN pip install "setuptools>=65.5.1"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/workdir

COPY bin/scripts/entrypoint.sh ./bin/scripts/entrypoint.sh
COPY bin/scripts/system.sh ./bin/scripts/system.sh
# Install security updates and libpq-dev, which is required for psycopg2-binary,
# which is required for Saga; and latex + fonts, which are required for report PDFs

# Copy the dependency files
COPY pyproject.toml poetry.lock /workdir/
COPY src/kassett_actions /workdir/kassett_actions

FROM base as build-base
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_VERSION=21.3.1 \
    POETRY_VERSION=1.7.1

RUN ./bin/scripts/system.sh \
    build-essential \
    git \
    ssh

RUN mkdir -p ~/.ssh && ssh-keyscan -t rsa github.com > ~/.ssh/known_hosts
RUN python -m pip install "pip==$PIP_VERSION"
RUN pip install "poetry==$POETRY_VERSION"


FROM build-base AS dev
RUN --mount=type=ssh poetry export --without-hashes --with=dev -o dependencies.txt
RUN --mount=type=ssh pip install -r dependencies.txt

COPY src/tests /workdir/tests/

ENTRYPOINT ["/bin/bash", "/workdir/bin/scripts/entrypoint.sh"]