#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

# The crash address in little endian
crash_bytes = p32(0x61616461)
print(f"Crash bytes (little endian): {crash_bytes}")
print(f"As string: {crash_bytes.decode('latin1')}")

# Generate pattern
pattern2 = cyclic(28, n=8)
print(f"\nPattern 2: {pattern2}")
print(f"Pattern 2 hex: {pattern2.hex()}")

# Find where these bytes appear
if crash_bytes in pattern2:
    offset = pattern2.index(crash_bytes)
    print(f"\nFound at offset: {offset}")
else:
    print("\nNot found in pattern2")
    # Try with 4-byte pattern instead
    pattern2_n4 = cyclic(28, n=4)
    print(f"\nPattern 2 (n=4): {pattern2_n4}")
    print(f"Pattern 2 (n=4) hex: {pattern2_n4.hex()}")
    if crash_bytes in pattern2_n4:
        offset = pattern2_n4.index(crash_bytes)
        print(f"Found at offset: {offset}")
