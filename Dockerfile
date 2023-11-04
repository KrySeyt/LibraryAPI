FROM python:3.11.4-slim-bullseye
RUN apt-get update
RUN rm -rf /var/lib/apt

ENV WORKDIR=/LibraryAPI

WORKDIR $WORKDIR

ENV VIRTUAL_ENV="$WORKDIR/venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python -m venv $VIRTUAL_ENV

COPY pyproject.toml pyproject.toml
COPY src/ src/
COPY alembic/ alembic/
COPY alembic.ini alembic.ini

RUN pip install -e . --no-cache-dir

CMD alembic upgrade head && python -O -m gunicorn -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker libraryapi.main.api:app 
