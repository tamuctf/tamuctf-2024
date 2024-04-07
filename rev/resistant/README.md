# Resistant

Author: `tacex`

All these RE challenges are just too easy! So what happens when the binary fights back?

## Solution

The provided binary runs a function called `check_debug` before running `decrypt_func`. If `check_debug` fails, `decrypt_func` is not run. The `check_debug` logic can be nop'd out so that a debugger can be used to view the `decrypt_func` call and the subsequent call to auth. If you try to statically reverse the auth function, it is clear that it is not valid assembly. It can be assumed using this information that auth is the function being decrypted.

Since the debug check is patched out, a breakpoint can be set right before auth is called to get the decrypted assembly of `auth`. In `auth`, `memcmp` is called before a conditional statement which either prints a message and exits or opens a file. It can be assumed that this is where the user input is compared to a password, so a breakpoint can be set there to see the plaintext password, `N0tUrM0msP4sswd!`.

Flag: `gigem{a_b4ttl3_4_th3_hist0ry_b00ks}`
