#!/usr/bin/env sh

set -m

cleanup() {
  trap "" INT TERM EXIT
  kill -9 ${pid} 2>/dev/null || true
  exit 0
}

trap cleanup INT TERM EXIT

echo
echo '-------------------------------------------------------------------------'
echo "booting! please wait ~15 seconds"
echo '-------------------------------------------------------------------------'
echo

while true; do
  port=$(shuf -n 1 -i 49152-65535)
  timeout 1 nc -l -n "$port"
  if [ $? -eq 124 ]; then
    break
  fi
done

qemu-system-x86_64 -accel kvm -monitor none -display none -drive file=/over-the-shoulder.qcow2,format=qcow2,snapshot=on -machine q35,usb=off,dump-guest-core=off,hpet=off,acpi=on -m 512M -netdev user,id=user.0,hostfwd=tcp::${port}-:1337 -device e1000,netdev=user.0 &
pid=$!

sleep .5 # dodge a confusing connection refused

while ! socat -s - tcp:localhost:${port}; do
  sleep .5
done
