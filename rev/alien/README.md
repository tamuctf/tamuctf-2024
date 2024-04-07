# Alien

Author: `Addison`

Run the lm3s6965 firmware. Press enter to let it know you're listening. Read the flag.

## Solution

As the challenge description states, this is lm3s6965 firmware.

As this is firmware built for a specific hardware environment, we will need to emulate the hardware environment with qemu.

![The Rust Book](https://docs.rust-embedded.org/book/start/qemu.html) contains a great tutorial of using QEMU to run firmware for embedded systems.

The book provides us with a command to execute to run a binary which conveniently uses the same architecture.

```bash
qemu-system-arm \
  -cpu cortex-m3 \
  -machine lm3s6965evb \
  -nographic \
  -semihosting-config enable=on,target=native \
  -gdb tcp::3333 \
  -S \
  -kernel target/thumbv7m-none-eabi/debug/examples/hello
```

We can modify this command to execute our code using:

```bash
qemu-system-arm \
  -cpu cortex-m3 \
  -machine lm3s6965evb \
  -nographic \
  -semihosting-config enable=on,target=native \
  -kernel ./alien.elf
```

Running this command and hitting enter will provide us with the flag.

Flag: `gigem{https://www.youtube.com/watch?v=7Vb1BBpWe0w}`
