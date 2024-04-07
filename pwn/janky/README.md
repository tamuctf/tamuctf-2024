# Janky

Author: `nhwn`

Pwn isn't fun if your solve isn't janky.

## Solution

In `validate`, each instruction mnemonic of our shellcode payload is required to start with the letter `j` (otherwise, our payload doesn't run). Given this restriction, we only have `jmp` (and its conditional variants) to work with. To get arbitrary code execution, we can abuse how the destination immediate of a `jmp` instruction is an attacker-controlled value that can be jumped to. By repeatedly jumping into immediates, we can execute arbitrary payloads of arbitrary length in chunks of 4 bytes at a time (the largest immediate that can be specified is 32 bits). The final exploit in `solve.py` runs a `read` payload to load in off-the-shelf shellcode, then jumps to it.

Flag: `gigem{jump1ng_thr0ugh_h00p5}`
