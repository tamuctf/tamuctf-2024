from pwn import *

context.log_level = "debug"
io = remote("tamuctf.com", 443, ssl=True, sni="smooth-signatures")
io.interactive(prompt="")
