from pathlib import Path
from base64 import b64decode
from Crypto.PublicKey import RSA


key = Path("private.pem").read_text()

strip = "".join(key.splitlines()[:-1])
leak = b64decode(strip)
q = leak.split(b"\x02\x81")[1:-1][0]

q  = int.from_bytes(q[1:], byteorder="big")

print(f"q = {q}")
