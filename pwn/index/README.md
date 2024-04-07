# Index

Author: `nhwn`

I added bounds checking to my array accesses, so good luck getting the flag now!

## Solution

Our goal is to override control flow and get to the provided `win` function. There's a potential stack buffer overflow via the `strcpy` here:

```c
puts("Enter an index to read (0-2):");
Message tmp;
strcpy(tmp, get_message(get()));
puts(tmp);
```

Looking at the disassembly, we need the source string to contain at least 0x80 + 8 + 8 = 144 bytes to corrupt the return address:

```
40139f:	lea    rax,[rbp-0x80]
4013a3:	mov    rsi,rdx
4013a6:	mov    rdi,rax
4013a9:	call   401030 <strcpy@plt>
```

Unfortunately, we can only set up to 99 bytes at a time (excluding the null terminator) for each `Message` struct. Furthermore, the bounds check in `get_message` prevents us from picking arbitrary memory locations to treat as source strings:

```c
char* get_message(unsigned long i) {
    Message* ret = &MESSAGES[i];
    Message* start = &MESSAGES[0];
    Message* end = &MESSAGES[2];
    if (ret < start || end < ret) {
        puts("That's not allowed!");
        exit(0);
    }
    return ret;
}
```

However, not all hope is lost; the bounds check fails to prevent us from providing an index whose corresponding pointer ends up _between_ intended messages. In particular, we can set a `Message` that's misaligned inside the `MESSAGES` array such that the offset preceding `Message`'s null terminator will exceed the 100 byte limit.

To actually compute the correct index, we can use some math (brute-force or z3 would also work). For any congruence ax = b (mod n) where gcd(a, n) = 1, we can just multiply by the multiplicative inverse of a. In our case, we have a = 100, n = 2^64, and b is some unspecified offset (in bytes) into `MESSAGES`. Unfortunately, g = gcd(a, n) = 4, so the multiplicative inverse doesn't exist. To rectify this, we can transform the congruence into (a / g) x = (b / g) (mod (n / g)), as long as g divides b. Then, we can pick b = 96 to create a string of length 96 + 99 = 195, which is more than enough to overwrite the return address.

See `solve.py` for the full solve.

Flag: `gigem{wh0_put_m4th_1n_my_pwn}`
