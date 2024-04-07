from pwn import *
from math import gcd, lcm
flag = 0
iterations = 100
mod_6 = [0]*6
for _ in range(iterations):
    #p = process("python3 qcg.py",shell=True)
    p = remote("localhost", 1337)
    x = [int(p.recvline().decode()) for _ in range(10)]
    y = []
    b_y = []
    c_y = []
    for i in range(len(x)-1):
        for j in range(i):
            mult = gcd(x[i]**2,x[j]**2)
            y.append(x[i]**2//mult*x[j+1] - x[j]**2//mult*x[i+1])
            b_y.append(x[i]**2//mult*x[j] - x[j]**2//mult*x[i])
            c_y.append(x[i]**2//mult - x[j]**2//mult)
    z = []
    c_z = []
    for i in range(len(y)):
        for j in range(i):
            mult = gcd(b_y[j],b_y[i])
            z.append(y[i]*b_y[j]//mult-y[j]*b_y[i]//mult)
            c_z.append(c_y[i]*b_y[j]//mult-c_y[j]*b_y[i]//mult)
    m_mults = []
    for i in range(len(z)):
        for j in range(i):
            mult = gcd(c_z[j],c_z[i])
            m_mults.append(z[i]*c_z[j]//mult-z[j]*c_z[i]//mult)
    gcf = m_mults[0]
    for val in m_mults:
        gcf = gcd(gcf,val)
    m = gcf
    print(f"{m = }")
    print(f"{m % 6 = }")
    c_found = False
    index = 0
    while not c_found:
        try:
            c = pow(c_z[index] % m,-1,m) * z[index] % m
            c_found = True
        except:
            index += 1
            if index == len(z):
                p.close()
                break
                #exit()
            continue
    if not c_found:
        continue
    print(f"{c = }")
    
    index = 0
    b_found = False
    while not b_found:
        try:
            b = pow(b_y[index] % m,-1,m) * (y[index] - c*c_y[index]) % m
            b_found = True
        except:
            index += 1
            if index == len(y):
                p.close()
                break
                #exit()
            continue
    if not b_found:
        continue
    print(f"{b = }")

    index = 0
    a_found = False
    while not a_found:
        try:
            a = pow(x[index]**2 % m,-1,m) * (x[index+1] - b*x[index] - c) % m
            a_found = True
        except:
            index += 1
            if index == len(x)-1:
                p.close()
                break
                #exit()
            continue
    if not a_found:
        continue
    print(f"{a = }")

    class QCG:
        def __init__(self,m,a,b,c,x):
            self.m = m
            self.a = a
            self.b = b
            self.c = c
            self.x = x
        def __call__(self):
            self.x = (self.a*self.x**2+self.b*self.x+self.c) % self.m
            return self.x
        def generate_value(self,seed):
            return (self.a*seed**2+self.b*seed+self.c) % self.m
        def printm(self):
            print(self.m)
            return

    qcg = QCG(m,a,b,c,x[-1])
    for i in range(5):
        p.sendline(str(qcg()).encode())
    result = p.recvline()
    if b"failed" not in result:
        mod_6[m%6] += 1
        flag += 1
        print("success: \n" + result.decode())
        exit()
    p.close()
print(flag / iterations)
print(mod_6)
