#!/usr/bin/env python3

import struct

# Read config.bin
with open('/workspace/config.bin', 'rb') as f:
    data = f.read()

# First 4 bytes are the length
length = struct.unpack('<I', data[0:4])[0]
flag_data = bytearray(data[4:4+length])
xor_key = data[4+length:]

print(f"Length: {length}")
print(f"Flag data: {flag_data.decode('ascii')}")
print(f"XOR key (hex): {xor_key.hex()}")

# First XOR the flag_data with xor_key
# Based on the function at 0x402cb0 (fcn.0040127b)
for i in range(min(len(flag_data), len(xor_key))):
    flag_data[i] ^= xor_key[i]

print(f"\nAfter XOR: {flag_data}")
try:
    print(f"After XOR (ASCII): {flag_data.decode('ascii', errors='ignore')}")
except:
    pass

# Now reverse the algorithm in fcn.0040122b (at 0x402bc0)
# This is the decryption function that reverses the obfuscation
# Based on the assembly, here's what it does:
# var_10h = 0x55  # 85
# var_18h = 0x33  # 51
# var_20h = 0x0f  # 15
# var_1h = 0x61   # 'a'

# The algorithm processes each byte and applies transformations
# We need to reverse it

# Let's try the reverse process
VAR_10 = 0x55
VAR_18 = 0x33
VAR_20 = 0x0f
VAR_1 = ord('a')

decrypted = bytearray(flag_data)

# The algorithm in the assembly seems to be encrypting, not decrypting
# We need to reverse it
# Let's try the direct interpretation first

print("\n=== Trying to interpret as picoCTF flag ===")
# The flag format is picoCTF{...}
# Let's see if there's a pattern

# Try simple Caesar cipher on the original data
original_flag = data[4:4+length]
for shift in range(26):
    decoded = ""
    for b in original_flag:
        if ord('a') <= b <= ord('z'):
            decoded += chr((b - ord('a') + shift) % 26 + ord('a'))
        elif ord('A') <= b <= ord('Z'):
            decoded += chr((b - ord('A') + shift) % 26 + ord('A'))
        else:
            decoded += chr(b)
    if decoded.startswith('picoctf') or decoded.startswith('picoCTF'):
        print(f"Shift {shift}: {decoded}")
        break

# Try with initial 'p' being at a certain position
target_first = ord('p')
actual_first = original_flag[0]
if ord('a') <= actual_first <= ord('z'):
    shift = (actual_first - target_first) % 26
    print(f"\nCalculated shift from first char: {shift}")
    decoded = ""
    for b in original_flag:
        if ord('a') <= b <= ord('z'):
            decoded += chr((b - ord('a') - shift) % 26 + ord('a'))
        elif ord('A') <= b <= ord('Z'):
            decoded += chr((b - ord('A') - shift) % 26 + ord('A'))
        else:
            decoded += chr(b)
    print(f"Decoded: {decoded}")
