FROM python:slim-buster

ARG port

RUN apt-get update -y; apt-get install socat -y

COPY flag.txt /crypto/flag.txt
COPY pcg.py /crypto/pcg.py
RUN chmod +x /crypto/pcg.py
RUN python3 -m pip install pycryptodome
WORKDIR /crypto
EXPOSE $port

RUN echo "exec socat -s TCP-LISTEN:$port,reuseaddr,fork EXEC:'python3 /crypto/pcg.py',stderr" > /crypto/docker_entrypoint.sh

ENTRYPOINT ["sh", "/crypto/docker_entrypoint.sh"]
