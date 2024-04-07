from pathlib import Path
from base64 import b64decode
from Crypto.PublicKey import RSA


key = Path("private.pem").read_text()
pub = RSA.importKey(Path("public.pem").read_text())
strip = "".join(key.splitlines()[:-1])
leak = b64decode(strip)
dp, dq = leak.split(b"\x02\x81")[1:-1]
dp = int.from_bytes(dp[1:], byteorder="big")
dq = int.from_bytes(dq[1:], byteorder="big")
print(f"dp = {dp}")
print(f"dq = {dq}")