# Over The Shoulder

Author: `Addison`

You are given a shell inside a docker container. The host running docker does `cat /home/user/flag.txt` once per minute. Read the flag.

## Hosting Notes

Download here: https://drive.google.com/file/d/1aFhTmzd_NZiorq5zZEA9TT3etpwd58iv/view?usp=sharing

The QEMU machine needs about 1GB per connection.
There's a fairly hefty proof of work in front of each connection to reduce the pain here.

My command line for starting it looks something like this:
```
docker run --rm -ti --privileged -p 5000:5000 over-the-shoulder
```

Note especially:
 - `--privileged` is required by redpwn/kvm
 - port 5000 is the interior port mapping

## Solution

This challenge looks like so:

```
host
 |
 | // spawned per connection
 v
qemu
 |
 |
 v
docker container w/ cap_bpf,cap_perfmon
```

Attackers must leverage `CAP_BPF`/`CAP_PERFMON` to read the flag.
This is completed in `solver/` by creating a BPF program which dumps all strings passed to `write` with fd 1 by any process named `cat`.

To use the solver, install Rust, then:
 - `rustup target add x86_64-unknown-linux-musl`
 - `cargo install bpf-linker`
 - `./solve.sh`

The solver binary will be built for you, just paste the redpwn challenge when prompted.

Flag: `gigem{this_aint_your_mamas_shoulder_surfing}`
