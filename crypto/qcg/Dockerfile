FROM debian:buster-slim

ARG port

RUN apt-get update -y; apt-get install python3 socat -y
ADD qcg.py /chal/qcg.py
ADD flag.txt /chal/flag.txt

WORKDIR /chal

RUN echo "exec socat -s TCP-LISTEN:$port,reuseaddr,fork EXEC:'python3 qcg.py,stderr'" > /chal/docker_entrypoint.sh

ENTRYPOINT ["sh", "/chal/docker_entrypoint.sh"]
