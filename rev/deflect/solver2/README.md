# solver2

This is not the right way, but it is a fun way.

## Prerequisites

1. Install bpf-linker: `cargo install bpf-linker`

## Run

```
RUST_LOG=info cargo xtask run --release
```

or, if connected by VPN

```
RUST_LOG=info cargo xtask run --release --features tun
```

Then, in a second window (replace 1.2.3.4 accordingly):

```
curl --local-port http://1.2.3.4
```
