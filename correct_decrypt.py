#!/usr/bin/env python3

import struct

# Read config.bin
with open('/workspace/config.bin', 'rb') as f:
    data = f.read()

# Parse the file
length = struct.unpack('<I', data[0:4])[0]

encrypted_flag = bytearray(data[4:4+length])
xor_key_start = 4 + length
expected_xor_len = length * 2 + 2
xor_key = bytearray(data[xor_key_start:xor_key_start+expected_xor_len])

print(f"Length: {length}")
print(f"Encrypted flag: {encrypted_flag.decode('ascii')}")
print(f"XOR key length: {len(xor_key)}")

# Based on the assembly code analysis:
# 1. fcn.0040122b (at 0x4037b8) is called with arg 2 - this obfuscates the FLAG data (at 0x40c3d0)
# 2. fcn.0040127b (at 0x4038f1) is called with the FLAG pointer - this XORs KEY with FLAG
#    The function does: KEY[i] ^= FLAG[i], so it modifies the KEY, not the FLAG
# 3. The final result is in the KEY (at 0x40c3d4)

def apply_obfuscation(data, iterations):
    """Apply the obfuscation algorithm"""
    result = bytearray(data)
    
    VAR_10 = 0x55
    VAR_18 = 0x33
    VAR_20 = 0x0F
    VAR_1 = ord('a')
    
    for iteration in range(iterations):
        for i in range(len(result)):
            idx_mod = i % 0xFF
            temp1 = (idx_mod & VAR_10) + ((idx_mod >> 1) & VAR_10)
            temp2 = (temp1 & VAR_18) + ((temp1 >> 2) & VAR_18)
            
            current = result[i]
            value = current - VAR_1
            value += (temp2 & VAR_20) + ((temp2 >> 4) & VAR_20)
            new_value = VAR_1 + (value % 26)
            result[i] = new_value
    
    return result

# Step 1: Obfuscate the flag (fcn.0040122b with arg 2)
obfuscated_flag = apply_obfuscation(encrypted_flag, 2)
print(f"\nAfter obfuscation: {obfuscated_flag.decode('ascii')}")

# Step 2: XOR the key with the obfuscated flag (fcn.0040127b)
# The function does: xor_key[i] ^= obfuscated_flag[i]
result_key = bytearray(xor_key)
for i in range(min(len(result_key), len(obfuscated_flag))):
    result_key[i] ^= obfuscated_flag[i]

print(f"\nAfter XOR (hex): {result_key.hex()}")
print(f"After XOR (raw): {result_key}")

# Try to decode
try:
    decoded = result_key.decode('utf-16-le', errors='ignore')
    print(f"\nDecoded (UTF-16-LE): {decoded}")
except:
    pass

try:
    decoded = result_key.decode('ascii', errors='ignore')
    print(f"Decoded (ASCII): {decoded}")
except:
    pass

# Also try as wide char (2 bytes per char)
wide_chars = []
for i in range(0, len(result_key)-1, 2):
    char_code = struct.unpack('<H', result_key[i:i+2])[0]
    if 32 <= char_code < 127:
        wide_chars.append(chr(char_code))
    else:
        wide_chars.append(f'\\x{char_code:04x}')

wide_string = ''.join(wide_chars)
print(f"Wide char interpretation: {wide_string}")
