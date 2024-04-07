from pwn import remote
from base64 import b64decode

alphabet = "abcdefghijklmnopqrstuvwxyz_}"
flag = "gigem{"
p = remote("localhost", 1337)

def get(c):
    guess = flag.encode() + c.encode()
    p.sendline(guess)
    p.recvuntil(b": ")
    n = len(b64decode(p.recvline()))
    return c, n

while True:
    best, _ = min((get(c) for c in alphabet), key=lambda x: x[1])
    flag += best
    if best == "}":
        break

print(flag)
