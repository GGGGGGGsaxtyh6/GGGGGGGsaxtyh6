#!/usr/bin/env python3

import struct

# Read config.bin
with open('/workspace/config.bin', 'rb') as f:
    data = f.read()

# First 4 bytes are the length
length = struct.unpack('<I', data[0:4])[0]
print(f"Length: {length}")

# The actual flag data starts at offset 4
flag_data = data[4:4+length]
print(f"Flag data (hex): {flag_data.hex()}")
print(f"Flag data (raw): {flag_data}")

# Looking at the disassembly, the function at 0x402bc0 (fcn.0040122b) 
# processes the data with some algorithm. Let me try to decrypt it
# by analyzing the algorithm.

# The function at 0x402cb0 does XOR with some data
# Let's see if there's a simple pattern

# Try to decode as ASCII with different offsets
for offset in range(26):
    decoded = bytes([(b - offset) % 26 + ord('a') if b >= ord('a') and b <= ord('z') else b for b in flag_data])
    if b'pico' in decoded.lower() or b'CTF' in decoded or b'flag' in decoded.lower():
        print(f"Offset {offset}: {decoded}")

# Try ROT13-like transformations
print("\n=== Trying simple shifts ===")
for shift in range(1, 26):
    decoded = ""
    for b in flag_data:
        if ord('a') <= b <= ord('z'):
            decoded += chr((b - ord('a') - shift) % 26 + ord('a'))
        elif ord('A') <= b <= ord('Z'):
            decoded += chr((b - ord('A') - shift) % 26 + ord('A'))
        else:
            decoded += chr(b)
    if 'pico' in decoded.lower() or 'flag' in decoded.lower():
        print(f"Shift {shift}: {decoded}")

# Look at the XOR key from the second part of config.bin
xor_key = data[4+length:]
print(f"\n=== XOR key data: {xor_key.hex()} ===")

# Try XORing the flag data with the XOR key
if len(xor_key) > 0:
    decoded = bytearray()
    for i, b in enumerate(flag_data):
        key_byte = xor_key[i % len(xor_key)]
        decoded.append(b ^ key_byte)
    print(f"XOR decoded: {decoded}")
    try:
        print(f"XOR decoded (UTF-8): {decoded.decode('utf-8', errors='ignore')}")
    except:
        pass
