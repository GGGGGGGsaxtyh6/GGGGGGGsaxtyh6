#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

# Generate pattern
pattern = cyclic(28, n=8)

print("Pattern bytes:")
for i in range(28):
    print(f"Position {i:2d}: 0x{pattern[i]:02x} ('{chr(pattern[i])}')")

print("\nBytes 23-26 as little endian 32-bit value:")
val = u32(pattern[23:27])
print(f"Value: 0x{val:08x}")

print("\nBytes 24-27 as little endian 32-bit value:")
val2 = u32(pattern[24:28])
print(f"Value: 0x{val2:08x}")
