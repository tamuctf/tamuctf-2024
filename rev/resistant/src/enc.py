import sys
import struct
import secrets
import subprocess as sp

file = sys.argv[1]
elf = open(file, 'rb+')
data = elf.read()
secs = sp.check_output(f"nm -S {file}".split(' ')).decode().split('\n')

auth_addr = 0
auth_len = 0
dec_addr = 0
dec_len = 0

for row in secs:
    if 'T auth' in row:
        row = row.split(' ')
        auth_addr = int(row[0], 16)
        auth_len = int(row[1], 16)
    if 'T dec' in row:
        row = row.split(' ')
        dec_addr = int(row[0], 16)
        dec_len = int(row[1], 16)

auth_var = data.find(struct.pack('<Q', 0x123456789))
dec_var = data.find(struct.pack('<Q', 0x987654321))
key_var = data.find(b'0123456789ABCDEF')

key = secrets.token_bytes(16)

elf.seek(key_var)
elf.write(key)
elf.seek(dec_var)
elf.write(struct.pack('<Q', dec_len))
elf.seek(auth_var)
elf.write(struct.pack('<Q', auth_len))

elf.seek(auth_addr)
auth = bytearray(elf.read(auth_len))
elf.seek(dec_addr)
dec = bytearray(elf.read(dec_len))

for i in range(auth_len):
    auth[i] = auth[i] ^ key[i % 16]

for i in range(dec_len):
    dec[i] = dec[i] ^ key[i % 16]

elf.seek(auth_addr)
elf.write(auth)
elf.seek(dec_addr)
elf.write(dec)

print(f"Function key: {hex(key_var)} - 0x{key.hex()}")
print(f"Auth function: {hex(auth_addr)} - {hex(auth_var)} - {hex(auth_len)}")
print(f"Dec function: {hex(dec_addr)} - {hex(dec_var)} - {hex(dec_len)}")
