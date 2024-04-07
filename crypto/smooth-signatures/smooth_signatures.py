from Crypto.Util.number import getPrime,long_to_bytes,bytes_to_long
from math import lcm,gcd
from secrets import randbelow
from hashlib import sha256

NUM_BITS = 2048

def getModulus(bits):
    n = 1
    primes = []
    while n.bit_length() < bits:
        p = getPrime(24)
        if p not in primes:
            n *= p
            primes.append(p)
    return n,primes

def sign(n,msg,d):
    h = bytes_to_long(sha256(msg).digest())
    k = randbelow(q-2)+1
    x = pow(h,k,n)
    r = pow(x,d,n)
    s = pow(h+x,d,n)
    return r,s

def verify(n,msg,e,r,s):
    h = bytes_to_long(sha256(msg).digest())
    v1 = pow(r,e,n)
    v2 = pow(s,e,n)
    return v2 == (v1 + h) % n

n,primes = getModulus(NUM_BITS)
q = 1
for p in primes:
    q = lcm(q,p-1)
msgs = []
e = 65537
d = pow(e,-1,q)

print(f"The modulus is ... a mystery left for you to unfold.")
print(f"Your verification exponent {e = }")
msg = input("Give the oracle a message to sign: ").encode()
msgs.append(msg)
r,s = sign(n,msg,d)
print(f"Your verification signature is ({r}, {s})")

msg = input("Give the oracle another message to sign: ").encode()
msgs.append(msg)
r,s = sign(n,msg,d)
print(f"Your second verification signature is ({r}, {s})")

comm = input("Ask the oracle a question: ").encode()
r,s = input("Give the verification signature: ").split(",")
r,s = int(r),int(s)

if comm in msgs:
    print("Hey, no cheating")
    exit()
if verify(n,comm,e,r,s):
    if comm == b"What is the flag?":
        print("The flag is: ",end="")
        with open("flag.txt","r") as flag:
            print(flag.read())
    else:
        print("Not the right question.")
else:
    print("Invalid signature")
