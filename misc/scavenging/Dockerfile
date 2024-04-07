FROM ubuntu:latest as build

# because, for some reason, installers need to be interactive
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN sed -i 's/# deb-src/deb-src/g' /etc/apt/sources.list
RUN apt update && \
    apt -y --autoremove full-upgrade && \
    apt -y --autoremove install git curl && \
    apt -y build-dep linux

RUN cd /opt && \
    git clone --branch v6.7 --depth 1 https://github.com/torvalds/linux.git && \
    curl https://www.busybox.net/downloads/busybox-1.36.1.tar.bz2 | tar xjv

RUN cd /opt/linux && \
    make defconfig && \
    echo CONFIG_STRICT_DEVMEM=n >> /opt/linux/.config && \
    make -j$(nproc) bzImage vmlinux

ADD busybox.config /opt/busybox-1.36.1/.config
RUN cd /opt/busybox-1.36.1 && \
    make -j$(nproc) && make install && \
    mkdir -p /opt/rootfs && cd /opt/rootfs && \
    mkdir -p /opt/rootfs/inner && cd /opt/rootfs/inner && \
    mkdir -p bin sbin etc dev proc sys run usr/bin usr/sbin && \
    cp -a /opt/busybox-1.36.1/_install/* . && \
    cd .. && \
    mkdir dev proc sys run mnt && \
    ln -s inner/bin && ln -s inner/sbin && ln -s inner/etc

ADD init /opt/rootfs/init
ADD flag.txt /opt/rootfs/flag.txt

RUN cd /opt/rootfs && \
    find . -print0 | cpio --null -ov --format=newc | gzip -9 > /opt/initramfs.cpio.gz

FROM alpine:latest as app

RUN apk add --no-cache qemu-system-x86_64 socat
ADD entrypoint.sh /bin/entrypoint.sh

COPY --from=build /opt/initramfs.cpio.gz /opt/initramfs.cpio.gz
COPY --from=build /opt/linux/arch/x86/boot/bzImage /opt/bzImage

ARG port
ENV PORT ${port}

FROM pwn.red/jail

COPY --from=app / /srv

RUN rm -r /srv/var/tmp && ln -s /tmp /srv/var/tmp && mkdir /srv/app && ln -s /bin/entrypoint.sh /srv/app/run

ENV JAIL_POW=15000 JAIL_TMP_SIZE=1342177280 JAIL_DEV=null,zero,urandom JAIL_PIDS=0 JAIL_TIME=0 JAIL_MEM=0 JAIL_CPU=0
