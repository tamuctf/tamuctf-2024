# Criminal

Author: `nhwn`

It would be a crime for me to just give you the flag, so I'll encrypt it first before sending it. I'll even compress it to make it faster to transmit!

Note: the flag matches the regex `gigem{[a-z_]+}` (the curly braces are not quantifiers).

## Solution

The title of the challenge is a reference to the [CRIME](https://en.wikipedia.org/wiki/CRIME) attack, where information can be leaked about a compressed message if the attacker controls a portion of the message before compression and encryption. In particular, since compression exploits regularity in the input to reduce the length of the output, an input with common substrings will result in a smaller output (this is mostly independent of the encryption and compression algorithms used). We can use this behavior as an oracle; by brute-forcing one character at a time, we can check the resulting lengths of each response, then pick the one with the smallest length. This technique allows us to recover the flag in polynomial time.

See `solve.py` for the details.

Flag: `gigem{foiled_again}`
