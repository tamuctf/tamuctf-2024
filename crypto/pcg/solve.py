from pwn import *
from sage.all import *
from secrets import randbelow
from Crypto.Util.number import getPrime


context.log_level = "debug"
p = remote("localhost", 1337)
# p = process("python3 pcg.py", shell=True)
vals = []
m = int(p.recvline())
SIZE = 256
for i in range(SIZE*3):
    vals.append(int(p.recvline()))

F = GF(m)
A = Matrix(F,[[x**(SIZE-1-i) for i in range(SIZE)] for x in vals[:-1]])
y = vector(F,vals[1:])
arr = A.solve_right(y)
coeff = [int(x) for x in arr]
class PCG: # Polynomial Congruential Generator
    def __init__(self):
        self.m = getPrime(256)
        self.coeff = [randbelow(self.m-1) for _ in range(SIZE)]
        self.x = randbelow(self.m-1)
    def __call__(self):
        newx = 0
        for c in self.coeff:
            newx *= self.x
            newx += c
            newx %= self.m
        self.x = newx
        return self.x
    def printm(self):
        print(self.m)
        return
pcg = PCG()
pcg.m = m

pcg.coeff = coeff
pcg.x = vals[-1]
for i in range(SIZE // 2):
    p.sendline(str(pcg()).encode())
p.interactive()