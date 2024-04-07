# Smooth Signatures

Author: `GoldenBushRobin`

I've heard signatures are pretty good tools for verifying the sender. Signatures are supposed to be personalized and unique, so surely this one is impossible to forge... right?

## Solution

From the name of the challenge and the getModulus function, we can tell we are working with smooth numbers (numbers whose prime factors are at most some set value). Thus, if we can find the modulus or some multiple of the modulus, we can find its factors through brute force.

The signature is verified through `r^e + SHA256(msg) == s^e mod m`, so `r^e+sha(msg)-s^e == 0 mod m`
Thus, we can find a multiple of m through calculations.
I found that calculating `r^e` what extremely slow, so instead I calculated `r^e+sha(msg)-s^e` under all prime modulus within the valid range, and the values that are 0 are most likely factors of m.

From there, knowing the factors of the modulus, it is simple to follow the script in generating a signature.
Refer to `solve.py` for implementation.

Flag: `gigem{sm00th_numb3rs_4r3_345y_70_f4c70r}`
