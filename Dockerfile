FROM python:3.12

RUN apt-get update \
	&& apt-get -y install gcc \
	&& rm -rf /var/lib/apt/lists/*

ARG WORKDIR=/app


ENV \
        POETRY_VIRTUALENVS_CREATE=false \ 
        POETRY_VIRTUALENVS_IN_PROJECT=false \
        POETRY_NO_INTERACTION=1 \
        POETRY_VERSION=1.8.2

# install poetry
RUN pip install "poetry==${POETRY_VERSION}"

# set the working directory
WORKDIR $WORKDIR

# copy the requirements file to the container
COPY pyproject.toml poetry.lock* $WORKDIR

ENV PATH="/root/.poetry/bin:/root/.local/bin:$PATH"


# Install dependencies using poetry
RUN apt-get update && apt-get install -y curl \
    && pip install --upgrade pip setuptools uvicorn \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root --no-interaction --no-ansi

COPY . $WORKDIR

# Command to run FastAPI using Uvicorn
CMD ["poetry", "run", "uvicorn", "jamii.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]