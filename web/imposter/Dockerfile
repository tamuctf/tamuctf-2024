FROM python:3-alpine

RUN apk add --update --no-cache chromium chromium-chromedriver gcc musl-dev libffi-dev g++ && \
    pip install selenium Flask Flask-Session Flask-SQLAlchemy Flask-Login flask-socketio bcrypt && \
    adduser -D -u 1000 -g 1000 -s /bin/sh www && \
    mkdir -p /app

ARG flag
ARG port

ENV FLAG=${flag}
ENV PORT=${port}
ENV PYTHONDONTWRITEBYTECODE=1

COPY app/ /app
RUN chown -R www: /app

USER www
WORKDIR /app

RUN echo "flask run --host 0.0.0.0 --port ${PORT}" > /app/docker_entrypoint.sh

ENTRYPOINT ["sh", "/app/docker_entrypoint.sh"]
