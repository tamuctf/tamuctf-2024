# Flipped

Author: `tacex`

So many challenges have plaintext cookies. Try breaking my encrypted cookies!

## Solution

As the challenge name suggests, the session cookies are vulnerable to bit-flipping attacks because:

1. AES-128-CBC is used to encrypt/decrypt the session cookie (see https://crypto.stackexchange.com/questions/66085/bit-flipping-attack-on-cbc-mode for more info).
2. The server does not verify the integrity of the session cookie.

The flag is returned if the `admin` field in `{"admin": 0, "username": "guest"}` is non-zero, so the goal is to change that field. The initial session cookie has an ASCII zero (0x30) at offset 10, so we just need to flip the least-significant bit in the ciphertext byte to result in an ASCII one (0x31) for the corresponding plaintext byte.

```py
import requests
from base64 import b64decode, b64encode

url = "http://localhost:8000/"
default_session = '{"admin": 0, "username": "guest"}'
res = requests.get(url)
c = bytearray(b64decode(res.cookies["session"]))
c[default_session.index("0")] ^= 1
evil = b64encode(c).decode()
res = requests.get(url, cookies={"session": evil})
print(res.text)
```

Flag: `gigem{verify_your_cookies}`
