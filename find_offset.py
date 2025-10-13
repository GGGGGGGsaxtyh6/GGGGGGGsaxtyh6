#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

# Create cyclic patterns
pattern1 = cyclic(50)
pattern2 = cyclic(28, n=8)

print("Pattern 1 (50 bytes for first name):")
print(pattern1.hex())
print()
print("Pattern 2 (28 bytes for surname):")
print(pattern2.hex())
print()

# Save to file for testing
with open('/tmp/pattern_input', 'wb') as f:
    f.write(pattern1 + b'\n')
    f.write(pattern2 + b'\n')

print("Patterns saved to /tmp/pattern_input")
