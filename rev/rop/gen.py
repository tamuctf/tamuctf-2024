from pwn import *
from ctypes import CDLL
libc = CDLL("libc.so.6")
elf = ELF("./rop")
context.binary = elf

main = elf.sym["main"] + 8
seed = u32(elf.read(main, 4))
libc.srand(seed)
flag = b"gigem{i_<3_m3rs3nn3_pr1m35!}"
assert len(flag) == 28
flag_chunks = [int.from_bytes(flag[i:i + 7], byteorder="little") for i in range(0, 28, 7)]
encoded = [pow(37, f, 2 ** 61 - 1) for f in flag_chunks]
target = 0x0000000000500000
raw_gadgets = f"""
load:
    mov rdi, [rdi + rsi]
    ret

store:
    mov [rsi], rdi
    ret

reload:
    mov rdi, rax
    ret

equal:
    push rdi
    push rsi
    call {elf.sym["rand"]}
    pop rsi
    pop rdi
    xor rdi, rax
    xor rdi, rsi
    mov rdi, 0
    mov r9, 1
    cmovz rdi, r9
    xor esi, esi
    ret

call_rax:
    call rax
    ret

mov_rsi_rdi:
    mov rsi, rdi
    ret

mask:
    shl rdi, 8
    shr rdi, 8
    ret

modmul:
    mov rax, rdi
    mul rsi
    shl rdx, 3
    mov rdi, rax
    shr rax, 61
    or rdx, rax
    shl rdi, 3
    shr rdi, 3
    add rdi, rdx
    mov rax, rdi
    mov rsi, 2305843009213693951
    sub rax, rsi
    cmovge rdi, rax
    ret

modpow:
    mov rcx, 37
    mov r8, rdi
    mov r9, 1
modpow_loop:
    test r8, r8
    je modpow_done
    test r8, 1
    jz square
    mov rdi, r9
    mov rsi, rcx
    call modmul
    mov r9, rdi
square:
    mov rdi, rcx
    mov rsi, rcx
    call modmul
    mov rcx, rdi
    shr r8, 1
    jmp modpow_loop
modpow_done:
    mov rdi, r9
    ret

check:
    test rdi, rdi
    je almost_exit
    ret
almost_exit:
    test rsi, rsi
    je actual_exit
    mov rdi, rsi
    call {elf.sym["puts"]}
actual_exit:
    xor edi, edi
    jmp {elf.sym["exit"]}
usage_msg:
.asciz "Usage: ./rop FLAG"
yay_msg:
.asciz "That's the flag!"
guess:
actual_guess:
"""
gs = ELF.from_assembly(raw_gadgets, vma=target).sym
gadgets = asm(raw_gadgets, vma=target)

rop = ROP(elf)
rop.raw(b"\x00" * 72)
rop.mmap(target, 0x2000, 7, constants.MAP_ANONYMOUS | constants.MAP_PRIVATE, -1, 0)
rop.read(0, target, len(gadgets))
rop.memfrob(target, len(gadgets))

# init srand
rop.call(gs["load"], [main, 0])
rop.srand()
# get argv[1]
argv = elf.sym["__libc_argv"]
rop.call(gs["load"], [argv, 0])
rop(rsi=8)
rop.call(gs["load"])

# ensure argv[1] != NULL
rop(rsi=gs["usage_msg"])
rop.call(gs["check"])

# stash argv[1]
rop(rsi=gs["guess"])
rop.call(gs["store"])

# ensure strlen(argv[1]) == 28
rop.strlen()
rop.call(gs["call_rax"])
rop.call(gs["reload"])
rop(rsi=28 ^ libc.rand())
rop.call(gs["equal"])
rop.call(gs["check"])

# put argv[1] at a fixed address
rop.call(gs["load"], [gs["guess"], 0])
rop.call(gs["mov_rsi_rdi"])
rop(rdi=gs["actual_guess"])
rop.strcpy()
rop.call(gs["call_rax"])

for i in range(4):
    rop.call(gs["load"], [gs["actual_guess"], i * 7])
    rop.call(gs["mask"])
    rop.call(gs["modpow"])
    rop(rsi=encoded[i] ^ libc.rand())
    rop.call(gs["equal"])
    rop.call(gs["check"])

# win
rop.puts(gs["yay_msg"])
rop.exit(0)

chain = flat(rop.build(), filler=b"\x00")
def x(xs):
    return xor(xs, bytes([42]))
xord = x(gadgets)
out = chain + xord
print("chain", len(chain))
print("total bytes", len(out))
elf.write(next(elf.search(b"AAAA")), out)
elf.write(next(elf.search(b"iiii")), p32(len(chain)))
elf.save(elf.path)
