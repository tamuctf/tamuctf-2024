FROM python:3.8-slim

ARG port

RUN apt-get update -y; apt-get install socat -y
ADD emoji_group.py /chal/emoji_group.py
ADD flag.txt /chal/flag.txt
ADD secrets.py /chal/secrets.py

WORKDIR /chal

RUN echo "exec socat -s TCP-LISTEN:$port,reuseaddr,fork EXEC:'python3 emoji_group.py',stderr" > /chal/docker_entrypoint.sh

ENTRYPOINT ["sh", "/chal/docker_entrypoint.sh"]
