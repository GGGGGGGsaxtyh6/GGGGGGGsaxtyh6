#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

# The crash address
crash_addr = 0x61616461

# Find offset in the second pattern (n=8 for 64-bit)
pattern2 = cyclic(28, n=8)
offset = cyclic_find(crash_addr, n=8)

print(f"Crash address: {hex(crash_addr)}")
print(f"Offset in pattern 2: {offset}")

# Verify
print(f"\nPattern2[{offset}:{offset+4}] = {pattern2[offset:offset+4]}")
print(f"As hex: {pattern2[offset:offset+4].hex()}")
