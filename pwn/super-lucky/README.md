# Super Lucky

Author: `nhwn`

Just be super-duper lucky!

## Solution

Our goal is to calculate the next 7 calls to `rand`. The "free lucky numbers" code has no bounds check, so this gives us a read primitive:

```c
unsigned long pick = 0;
scanf("%lu", &pick);
printf("Here's lucky number #%d: %d\n", i + 1, lucky_numbers[pick]);
```

Unfortunately, the seed doesn't show up in memory following the call to `srand`, so we'll need to intelligently leak glibc's RNG state.

To leak libc state, we need the base address of libc. This can be obtained by leaking any of the active GOT entries with 2 reads (4 bytes each), then doing the usual offset arithmetic. Now that we have libc's base address, we need to understand libc's RNG implementation. A quick Google search for "libc rand algorithm" yields a [StackOverflow post](https://stackoverflow.com/questions/18634079/glibc-rand-function-implementation) as the top result. The post describes how libc contains two families of RNG algorithms: linear congruential generators and additive feedback generators. Quoting the SO post:

> When you set your seed using srand(), the size of the state is 128 bytes by default, so the second generator is used.

The SO post also provides a [helpful link](https://www.mscs.dal.ca/~selinger/random/) that describes how `srand` and `rand` work. Even better, the link provides source code that reimplements `rand` with a seed of 1. I've modified the print statement to show the input and output states for 7 `rand` calls:

```c
#include <stdio.h>

#define MAX 1000
#define seed 1

main() {
  int r[MAX];
  int i;

  r[0] = seed;
  for (i=1; i<31; i++) {
    r[i] = (16807LL * r[i-1]) % 2147483647;
    if (r[i] < 0) {
      r[i] += 2147483647;
    }
  }
  for (i=31; i<34; i++) {
    r[i] = r[i-31];
  }
  for (i=34; i<344; i++) {
    r[i] = r[i-31] + r[i-3];
  }
  for (i=344; i<344 + 7; i++) {
    r[i] = r[i-31] + r[i-3];
    printf("0x%08x + 0x%08x = 0x%08x (mod 2^32)\n", r[i-31], r[i-3], r[i]);
  }
}
```

Here's the output:

```
0x3e01511e + 0x991539b1 = 0xd7168acf (mod 2^32)
0x4e508aaa + 0x16a5bce3 = 0x64f6478d (mod 2^32)
0x61048c05 + 0x6774a4cd = 0xc87930d2 (mod 2^32)
0xf5500617 + 0xd7168acf = 0xcc6690e6 (mod 2^32)
0x846b7115 + 0x64f6478d = 0xe961b8a2 (mod 2^32)
0x6a19892c + 0xc87930d2 = 0x3292b9fe (mod 2^32)
0x896a97af + 0xcc6690e6 = 0x55d12895 (mod 2^32)
```

Our goal is to obtain the rightmost column via leaks and/or computation. After the third row, note that the middle column contains values from the previous computations because of the `r[i-3]` term. In total, we'll need 7 + 3 = 10 reads to leak enough values to compute the next 7 calls to `rand`.

Running the challenge in gdb (with the correct libc patched in), we can use `set $rdi=1` just before the call to `srand`, then use gef's [search-pattern](https://hugsy.github.io/gef/commands/search-pattern/) to find the exact addresses of where libc stores the desired values (we're guaranteed to find the values since the lagged Fibonacci generator requires the last 31 states to be stored _somewhere_). It's also possible to do this statically with Ghidra, but dynamic analysis is arguably less work. Since these offsets are fixed relative to libc's base address, we can reuse the offsets for any arbitrary seed. Once we have all 7 state values, it's just a matter of shifting right once to get the actual `rand` values.

The full solve is in `solve.py`.

Flag: `gigem{n0_on3_exp3ct5_the_l4gg3d_f1b0n4cc1}`
