#!/bin/sh

set -m

cleanup() {
  trap "" INT TERM EXIT
  kill -9 "${pid}" 2>/dev/null || true
  rm -rf "${socks}"
  exit 0
}

socks="$(mktemp -d)"
trap cleanup INT TERM EXIT

qemu-system-x86_64 -kernel /opt/bzImage -serial unix:"${socks}/entrypoint",server -initrd /opt/initramfs.cpio.gz -append "earlyprintk=serial,ttyS0 console=ttyS0" -monitor none -display none &
export pid=$!

sleep .5
while ! socat -s - unix-connect:"${socks}/entrypoint"; do
  sleep .5
done
