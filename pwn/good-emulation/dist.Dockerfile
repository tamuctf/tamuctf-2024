FROM debian:buster-slim@sha256:bc2704bca194bb10ea0b52b4313dc44fc3339cc648457fb18cb3509e71f199b7

RUN apt-get update -y; apt-get install build-essential gcc-arm-linux-gnueabi git libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev ninja-build socat -y
RUN git clone --depth 1 --branch v7.1.0 https://github.com/qemu/qemu.git
RUN cd qemu && ./configure --target-list=arm-linux-user && make
RUN cp /qemu/build/qemu-arm /usr/bin/qemu-arm
COPY good-emulation /pwn/good-emulation
WORKDIR /pwn

EXPOSE $port

RUN echo "exec socat -s TCP-LISTEN:1337,reuseaddr,fork EXEC:'qemu-arm /pwn/good-emulation',stderr" > /pwn/docker_entrypoint.sh

ENTRYPOINT ["sh", "/pwn/docker_entrypoint.sh"]
