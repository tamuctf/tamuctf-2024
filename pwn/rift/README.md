# Rift

Author: `nhwn`

You get a `printf`! You get a `printf`! Everyone gets a `printf`!

## Solution

We're in an (almost) infinite `printf` loop, but the controlled buffer is inside a global variable rather than on the stack, so we can't easily supply format strings for an arbitrary read or write. However, there are pointers on the stack that point to other pointers on the stack; we can use this to control the lower two bytes of a stack pointer using `%hn`. Now that we can write arbitrary values onto the stack, we can edit the return address of `vuln` to point to [one_gadget](https://github.com/david942j/one_gadget), then change the `always_true` variable to zero to exit the loop and trigger the gadget.

See `solve.py` for the full solve.

Flag: `gigem{ropping_in_style}`
