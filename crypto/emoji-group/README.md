# Emoji Group

Author: `GoldenBushRobin`

Emoji seem to have their own unique properties and strange combinations, so why not make a group out of them?

## Solution

The implementation of the encryption isn't all important, but what is, is that the ciphertext only has a single character unique nonce, and characters are encrypted separately. In addition, you can tell the oracle to encrypt "abcdef...".
Thus, we simply need to keep on querying until we find a match between our chosen plaintext's nonce and the flag's nonce. As the match does not need to be on the same round, this will take at most ~10-30 attempts to find a match.
For implementation details, see `solve.py`.

Flag: `gigem{h0p3_y0u_d1dn7_s0lv3_by_h4nd}`
