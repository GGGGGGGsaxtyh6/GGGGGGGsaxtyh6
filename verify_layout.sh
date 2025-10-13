#!/bin/bash

python3 << 'EOF'
from pwn import *
context.arch = 'amd64'

first_input = b'A' * 50
second_input = b'B' * 28

with open('/tmp/layout', 'wb') as f:
    f.write(first_input + second_input)
EOF

gdb -batch \
  -ex 'break *0x40076b' \
  -ex 'break *0x400798' \
  -ex 'run < /tmp/layout' \
  -ex 'printf "After first read:\n"' \
  -ex 'info registers rbp rsp rsi' \
  -ex 'x/20gx $rbp-0x60' \
  -ex 'continue' \
  -ex 'printf "\nAfter second read:\n"' \
  -ex 'info registers rbp rsp rsi' \
  -ex 'x/20gx $rbp-0x60' \
  ./stack_my_pivot 2>&1 | grep -A 30 "After"
