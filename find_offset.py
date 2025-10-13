#!/usr/bin/env python3
import struct
import sys

# Generate cyclic pattern
def cyclic(length):
    pattern = b""
    for i in range(length):
        pattern += bytes([65 + (i % 26)])
    return pattern

# Generate pattern of 200 bytes
pattern = cyclic(200)
sys.stdout.buffer.write(pattern)
