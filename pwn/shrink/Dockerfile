FROM debian:buster-slim as build

ARG name

RUN apt-get update -y; apt-get install build-essential -y
ADD $name.cpp /tmp/$name.cpp
ADD Makefile /tmp/Makefile
RUN cd /tmp/; make all

FROM debian:buster-slim

ARG name
ARG port

RUN apt-get update -y; apt-get install socat -y
COPY --from=build /tmp/$name /pwn/$name
COPY flag.txt /pwn/flag.txt
WORKDIR /pwn

EXPOSE $port

RUN echo "exec socat -s TCP-LISTEN:$port,reuseaddr,fork EXEC:'timeout -k 1 60 /pwn/$name,stderr'" > /pwn/docker_entrypoint.sh

ENTRYPOINT ["sh", "/pwn/docker_entrypoint.sh"]
