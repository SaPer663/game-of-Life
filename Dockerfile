FROM python:3.11.3-slim-bullseye as python

FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=production

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev
COPY ./requirements/base.txt .


RUN pip wheel --wheel-dir /usr/src/app/wheels  \
  -r base.txt


FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=production \
  APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/


COPY  . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
