FROM alpine:latest

RUN apk update --no-cache && \
    apk add --no-cache python3 py3-pip && \
    pip3 install --break-system-packages Flask pycryptodome 

ARG port
ARG flag

ENV PORT=${port}
ENV FLAG=${flag}
COPY src/ /app

ENTRYPOINT ["python3", "/app/app.py"]
