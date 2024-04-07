FROM debian:bullseye-slim as build

ARG name

RUN apt-get update -y; apt-get install build-essential gcc-arm-linux-gnueabi git libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev ninja-build -y
ADD $name.c /tmp/$name.c
ADD Makefile /tmp/Makefile
RUN cd /tmp/; make all
RUN git clone --depth 1 --branch v7.1.0 https://github.com/qemu/qemu.git
RUN cd qemu && ./configure --target-list=arm-linux-user && make

FROM debian:bullseye-slim

ARG name
ARG port

RUN apt-get update -y; apt-get install socat libglib2.0-dev -y
COPY --from=build /tmp/$name /pwn/$name
COPY --from=build /qemu/build/qemu-arm /usr/bin/qemu-arm
COPY flag.txt /pwn/flag.txt
WORKDIR /pwn

EXPOSE $port

RUN echo "exec socat -s TCP-LISTEN:$port,reuseaddr,fork EXEC:'timeout -k 1 60 qemu-arm /pwn/$name',stderr" > /pwn/docker_entrypoint.sh

ENTRYPOINT ["sh", "/pwn/docker_entrypoint.sh"]
