# Five

Author: `nhwn`

5-byte shellcode!?

## Hint

Check that your solve works in the provided Docker container before trying on remote.

## Solution

This challenge abuses some implementation details of `mmap` on Linux:

1. The specified address is a hint (we won't worry about `MAP_FIXED` or `MAP_FIXED_NOREPLACE`) and will be page-aligned.
2. If the address already belongs to a mapped region, the address will be assumed to be `NULL`. This will _not_ error out.
3. Calling `mmap` with a `NULL` address will pick a free region from some base address (ASLR will randomize this).
4. Libraries (e.g., libc) are initially loaded through `mmap` with a `NULL` address (check `strace`).

It's important to point out that the base address in #3 doesn't change between `mmap` calls. This means that regions created via `mmap(NULL, ...)` will always be at the same offsets (relative to each other) between different executions, even in the presence of ASLR (assuming the order in which they're mapped is the same).

Armed with this knowledge, our goal is to get a shell. The most direct method is via one_gadget:

```
0x4497f execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL
```

Looking at the jump from `main` into our payload, `rax` is already zeroed:

```
120e:	mov    eax,0x0
1213:	call   rdx
```

In other words, if we can do a relative jump into libc, we win. However, the `mmap` call throws a wrench in our plans:

```c
char* input = mmap(main + 0x10000, 0x1000, 7, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
```

This will place the region at an address that's too far away from libc for a relative jump (the largest relative jump offset is a signed 32-bit immediate). Fortunately, not all hope is lost. Since the payload is only roughly 0x10000 away from `main`, this is within the range of a relative jump. By jumping back to `main`, we get another 5-byte payload. The key difference from the initial throw is that `main + 0x10000` is _already mapped_, so when we go through `mmap` again, the target address will be interpreted as `NULL`. As a result, the second region will be loaded at a constant offset relative to libc (even with ASLR on!). To get the flag, it's then just a matter of doing another relative jump to the one_gadget.

See `solve.py` for the full solve.

Flag: `gigem{if_you_used_syscall_read_pls_tell_nhwn_how_you_did_it}`
