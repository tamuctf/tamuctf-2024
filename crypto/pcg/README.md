# PCG

Author: `GoldenBushRobin`

QCG seems a little too simple, so instead I rolled my own rng using polynomials.

## Solution

This challenge can be solved pretty simply using sage, mainly the below code.
```
for i in range(SIZE*3):
    vals.append(int(p.recvline()))

F = GF(m)
A = Matrix(F,[[x**(SIZE-1-i) for i in range(SIZE)] for x in vals[:-1]])
y = vector(F,vals[1:])
arr = A.solve_right(y)
```
The rest of the code is simply parsing in `solve.py`

Flag: `gigem{p0lyn0m1al5_4r3_funny}`
