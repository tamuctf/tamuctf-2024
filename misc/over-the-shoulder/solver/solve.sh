#!/bin/bash

cargo xtask build-ebpf --release && cargo build --release

(
 head -n 1; # for redpwn solving
 sleep 15; # wait for connection...
 echo 'cat <<THIS_IS_THE_END | base64 -d > solver';
 base64 target/x86_64-unknown-linux-musl/release/solver;
 echo THIS_IS_THE_END;
 echo chmod +x solver;
 echo 'RUST_LOG=info ./solver';
 while true; do echo keepalive; sleep 1; done
) | openssl s_client -connect tamuctf.com:443 -servername over-the-shoulder -quiet
