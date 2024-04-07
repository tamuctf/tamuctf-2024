FROM ubuntu:22.04

ARG name
ARG port

COPY src/* /
COPY flag.txt /

RUN apt update -y && \
    apt install -y libssl-dev build-essential socat python3-pip

RUN gcc ${name}.c -o ${name} -O0 -Wall -lssl -lcrypto -fcf-protection=branch -mmanual-endbr && \
    python3 enc.py ${name}

RUN echo "exec socat -s TCP-LISTEN:$port,reuseaddr,fork EXEC:/$name,stderr" > /docker_entrypoint.sh

ENTRYPOINT [ "sh", "/docker_entrypoint.sh" ]
