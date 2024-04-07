from pwn import *

messages = {}
flag_ct = {}
pt_nonces = set()
ct_nonces = set()
pt = "".join([chr(c) for c in range(0x20,0x7f)]).encode()
while len(pt_nonces & ct_nonces) == 0:
    p = remote("localhost",1337)
    p.sendlineafter(b"Give me a message to encrypt:",pt)
    
    p.recvuntil(b"Your cipher text is: ")
    ct = p.recvline().strip().decode()
    messages[ct[0]] = ct[1:]
    pt_nonces.add(ct[0])
    
    p.recvuntil(b"The flag is: ")
    f_ct = p.recvline().strip().decode()
    flag_ct[f_ct[0]] = f_ct[1:]
    ct_nonces.add(f_ct[0])
    p.close()

common = pt_nonces & ct_nonces
common_val = list(common)[0]
flag = ""
for c in flag_ct[common_val]:
    flag += chr(0x20+messages[common_val].index(c))
print(flag)
