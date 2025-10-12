#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

# Test local para entender el comportamiento
print("[*] Testing local binary...")

# Crear proceso
p = process('./handoff', timeout=5)

# Opción 1: Agregar una entrada
p.sendlineafter(b'3. Exit the app\n', b'1')
p.sendlineafter(b"What's the new recipient's name: \n", b'AAAAAAAA')

# Opción 2: Test índice negativo
p.sendlineafter(b'3. Exit the app\n', b'2')
p.sendlineafter(b'Which recipient would you like to send a message to?\n', b'-1')

# Ver si acepta índice negativo o da error
try:
    response = p.recvuntil([b'Invalid', b'What message'], timeout=2)
    print(f"[*] Response: {response}")
    
    if b'Invalid' in response:
        print("[-] Índice negativo rechazado")
    else:
        print("[+] Índice negativo ACEPTADO!")
        p.sendline(b'TESTMSG')
except:
    pass

p.close()
print("[*] Test completado")
