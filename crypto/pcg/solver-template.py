from pwn import *

context.log_level = "debug"
io = remote("tamuctf.com", 443, ssl=True, sni="pcg")
io.interactive(prompt="")
