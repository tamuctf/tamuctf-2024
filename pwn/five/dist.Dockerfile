FROM debian:buster-slim@sha256:bc2704bca194bb10ea0b52b4313dc44fc3339cc648457fb18cb3509e71f199b7

RUN apt-get update -y; apt-get install socat -y
COPY five /pwn/five
WORKDIR /pwn

EXPOSE 1337

RUN echo "it should just work on remote" >> /pwn/flag.txt
RUN echo "exec socat -s TCP-LISTEN:1337,reuseaddr,fork EXEC:/pwn/five,stderr" > /pwn/docker_entrypoint.sh

ENTRYPOINT ["sh", "/pwn/docker_entrypoint.sh"]
