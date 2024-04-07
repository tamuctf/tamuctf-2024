from Crypto.Util.number import getPrime,long_to_bytes,bytes_to_long,isPrime
from hashlib import sha256
import sys
from math import lcm,gcd
from secrets import randbelow
from tqdm import tqdm
from pwn import *

sys.set_int_max_str_digits(10**9)
e = 65537
p = remote("localhost",1337)
p.sendlineafter(b"Give the oracle a message to sign: ",b"hello world")
p.recvuntil(b"Your verification signature is (")
r,s = map(int,p.recvline().decode().strip()[:-1].split(", "))
p.sendlineafter(b"Give the oracle another message to sign: ",b"hello world")

msg = "hello world".encode()
h = bytes_to_long(sha256(msg).digest())
factors = []
print("Finding factors")
for i in tqdm(range(2**23,2**24)):
    if isPrime(i):
        ri = r % i
        si = s % i
        v1 = pow(ri,e,i)
        v2 = pow(si,e,i)
        if (v2 - v1 - h) % i == 0:
            # print(i)
            factors.append(i)
n = 1
q = 1
print(factors)
for f in factors:
    n *= f
    q = lcm(q,f-1)

e = 65537
d = pow(e,-1,q)


def sign(n,msg,d):
    h = bytes_to_long(sha256(msg).digest())
    k = randbelow(q-2)+1
    x = pow(h,k,n)
    r = pow(x,d,n)
    s = pow(h+x,d,n)
    return r,s
p.sendlineafter(b"Ask the oracle a question:",b"What is the flag?")
print("Forging the signature")
newr,news = sign(n,b"What is the flag?",d)
p.sendlineafter(b"Give the verification signature: ",f"{newr},{news}".encode())
print("Final result:")
p.interactive()

# print(n)
