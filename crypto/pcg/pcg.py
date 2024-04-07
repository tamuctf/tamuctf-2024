from secrets import randbelow
from Crypto.Util.number import getPrime
import sys

SIZE = 256
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

print(pcg.m)
for i in range(SIZE*3):
    print(pcg())

sys.stdout.flush()
correct = True
for i in range(SIZE // 2):
    guess = int(input())
    if guess != pcg():
        correct = False

if correct:
    print(open('flag.txt','r').read())
else:
    print("you failed")
sys.stdout.flush()
