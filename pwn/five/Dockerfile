FROM debian:buster-slim@sha256:bc2704bca194bb10ea0b52b4313dc44fc3339cc648457fb18cb3509e71f199b7 as build

ARG name

RUN apt-get update -y; apt-get install build-essential -y
ADD $name.c /tmp/$name.c
ADD Makefile /tmp/Makefile
RUN cd /tmp/; make all

FROM debian:buster-slim@sha256:bc2704bca194bb10ea0b52b4313dc44fc3339cc648457fb18cb3509e71f199b7

ARG name
ARG port

RUN apt-get update -y; apt-get install socat -y
COPY --from=build /tmp/$name /pwn/$name
COPY flag.txt /pwn/flag.txt
WORKDIR /pwn

EXPOSE $port

RUN echo "exec socat -s TCP-LISTEN:$port,reuseaddr,fork EXEC:'timeout -k 1 60 /pwn/$name,stderr'" > /pwn/docker_entrypoint.sh

ENTRYPOINT ["sh", "/pwn/docker_entrypoint.sh"]
