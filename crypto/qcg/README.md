# QCG

Author: `GoldenBushRobin`

Java uses LCG for random number generation, so I rolled my own random number generator, QCG. Surely it is more secure than LCD.

## Solution

The random number generator is using the formula:
`newstate == a*state^2 + b*state + c mod m, or newstate == a*state^2 + b* state + c + km`
The initial state, a, b, c, and m are all unknowns, and k can be any integer.
We are given 10 initial values, and we have to predict the next 5 states.
Thus, we have essentially a system of equations.
First, we need to find the modulus, which we can do by canceling out.

```
(as_i^2 + bs_i + c == s_i+1)s_j^2 - (as_j^2 + bs_j + c == s_j+1)s_i^2
= b(s_is_j^2-s_i^2s_j) + c(s_j^2-s_i^2) == (s_i+1)s_j^2 - (s_j+1)s_i^2
```

We repeat the process until we only have some sum of states equivalent to 0 mod m, which we take the gcd of.
From there we can simply put the system of equations as matrix-vector multiplication, and solve for the coefficients.

```
A = [[s_1^2,s_1,1],[s_2^2,s_2,1],...]
A * coeff = states[1:]
```

This can be done simply by throwing it into sage `solve_right`, or can be done by multiplying both sides by the transpose of A and inverting that product.
For more details or implementation, refer to `solve.py`.

Flag: `gigem{lcg_but_h4rd3r_101}`
