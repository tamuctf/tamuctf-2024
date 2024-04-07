FROM python:3.11-slim

ARG port

RUN apt-get update -y; apt-get install python3 python3-pip socat -y; pip3 install pycryptodome

ADD smooth_signatures.py /chal/smooth_signatures.py
ADD flag.txt /chal/flag.txt

WORKDIR /chal

RUN echo "exec socat -s TCP-LISTEN:$port,reuseaddr,fork EXEC:'python3 smooth_signatures.py',stderr" > /chal/docker_entrypoint.sh

ENTRYPOINT ["sh", "/chal/docker_entrypoint.sh"]
