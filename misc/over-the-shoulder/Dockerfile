FROM fedora as app

ADD over-the-shoulder.qcow2 /over-the-shoulder.qcow2

RUN dnf install -y qemu-system-x86 socat netcat
ADD entrypoint.sh /usr/local/bin/entrypoint.sh

FROM pwn.red/jail

COPY --from=app / /srv

RUN rm -r /srv/var/tmp && ln -s /tmp /srv/var/tmp && mkdir /srv/app && ln -s /usr/local/bin/entrypoint.sh /srv/app/run

ENV JAIL_POW=45000 JAIL_TMP_SIZE=68719476736 JAIL_DEV=null,zero,urandom,kvm JAIL_PIDS=0 JAIL_TIME=0 JAIL_MEM=0 JAIL_CPU=0
