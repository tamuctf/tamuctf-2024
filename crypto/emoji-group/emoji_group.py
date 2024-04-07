from secrets import multiply, g, identity, inverse, valid
from random import getrandbits

def power(p,x):
    out = identity
    while x:
        if x & 1:
            out = multiply(out,p)
        p = multiply(p,p)
        x >>= 1
    return out

def encrypt(msg,e):
    generator = power(g,e)
    out = generator
    for c in msg:
        out += power(generator,ord(c))
    return out

def decrypt(ct,d):
    chars = [power(g,i) for i in range(256)]
    plaintext = ""
    pt = power(ct[0],d)
    if pt != g:
        raise Exception("Invalid ciphertext")
    for c in ct[1:]:
        pt = power(c,d)
        plaintext += chr(chars.index(pt))
    return plaintext

print("Give me a message to encrypt:")
msg = input()
e = 0
while not valid(e):
    e = getrandbits(32)
ct = encrypt(msg,e)
print(f"Your cipher text is:",ct)
d = inverse(e)
print(f"The original message was:",decrypt(ct,d))

with open("flag.txt","r") as flag:
    e = 0
    while not valid(e):
        e = getrandbits(32)
    print("The flag is:",encrypt(flag.read(),e))