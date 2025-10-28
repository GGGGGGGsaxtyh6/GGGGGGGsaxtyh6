#!/usr/bin/env python3

import struct

# Read config.bin
with open('/workspace/config.bin', 'rb') as f:
    data = f.read()

# Parse the file
length = struct.unpack('<I', data[0:4])[0]
print(f"Length from file: {length}")

# The file format is:
# [4 bytes: length] [length bytes: encrypted flag] [remaining: xor key]
encrypted_flag = bytearray(data[4:4+length])
xor_key_start = 4 + length
# The XOR key length should be: length * 2 + 2
expected_xor_len = length * 2 + 2
xor_key = bytearray(data[xor_key_start:xor_key_start+expected_xor_len])

print(f"Encrypted flag ({len(encrypted_flag)} bytes): {encrypted_flag.decode('ascii')}")
print(f"XOR key ({len(xor_key)} bytes): {xor_key.hex()}")

# Step 1: Apply fcn.0040122b (the obfuscation function) with count=2
# This is called at 0x4037b8 with argument 2
def apply_obfuscation(data, iterations):
    """Apply the obfuscation algorithm from fcn.0040122b"""
    result = bytearray(data)
    
    VAR_10 = 0x55  # at ebp-0x10
    VAR_18 = 0x33  # at ebp-0x18
    VAR_20 = 0x0F  # at ebp-0x20
    VAR_1 = ord('a')  # at ebp-0x1
    
    data_len = length  # from [0x40c3d8]
    
    for iteration in range(iterations):
        for i in range(data_len):
            # Calculate temp values based on index
            # temp1 = ((i % 0xFF) & VAR_10) + (((i % 0xFF) >> 1) & VAR_10)
            idx_mod = i % 0xFF
            temp1 = (idx_mod & VAR_10) + ((idx_mod >> 1) & VAR_10)
            
            # temp2 = (temp1 & VAR_18) + ((temp1 >> 2) & VAR_18)
            temp2 = (temp1 & VAR_18) + ((temp1 >> 2) & VAR_18)
            
            # Get current byte value
            current = result[i]
            
            # value = (current - VAR_1) + (temp2 & VAR_20) + ((temp2 >> 4) & VAR_20)
            value = current - VAR_1
            value += (temp2 & VAR_20) + ((temp2 >> 4) & VAR_20)
            
            # new_value = VAR_1 + (value % 26)
            new_value = VAR_1 + (value % 26)
            result[i] = new_value
    
    return result

# Step 2: Apply XOR with the key (fcn.0040127b)
def apply_xor(data, key):
    """Apply XOR with the key"""
    result = bytearray(data)
    for i in range(min(len(result), len(key))):
        result[i] ^= key[i]
    return result

# Apply the transformations in the order they're called
print("\n=== Applying transformations ===")

# First, apply obfuscation with 2 iterations (called at 0x4037b8)
obfuscated = apply_obfuscation(encrypted_flag, 2)
print(f"After obfuscation (2 iterations): {obfuscated.decode('ascii', errors='ignore')}")

# Then apply XOR (called at 0x4038f1)
final_result = apply_xor(obfuscated, xor_key)
print(f"After XOR: {final_result.hex()}")
print(f"After XOR (raw): {final_result}")

# Try to decode as ASCII
try:
    decoded = final_result.decode('ascii', errors='ignore')
    print(f"Decoded: {decoded}")
except:
    decoded = final_result.decode('latin-1', errors='ignore')
    print(f"Decoded (latin-1): {decoded}")

# Also try the reverse: XOR first, then deobfuscate
print("\n=== Trying reverse order ===")
xored_first = apply_xor(encrypted_flag, xor_key)
print(f"XOR first: {xored_first.hex()}")

# Since the result contains non-letter characters, we need to handle them
# Convert to valid letter range for deobfuscation
def normalize_to_letters(data):
    result = bytearray()
    for b in data:
        if ord('a') <= b <= ord('z'):
            result.append(b)
        else:
            # Map to 'a' + (b % 26)
            result.append(ord('a') + (b % 26))
    return result

normalized = normalize_to_letters(xored_first)
print(f"Normalized: {normalized.decode('ascii')}")

# Try deobfuscating (reverse operation)
def reverse_obfuscation(data, iterations):
    """Reverse the obfuscation"""
    result = bytearray(data)
    
    VAR_10 = 0x55
    VAR_18 = 0x33
    VAR_20 = 0x0F
    VAR_1 = ord('a')
    
    data_len = len(result)
    
    for iteration in range(iterations):
        for i in range(data_len):
            idx_mod = i % 0xFF
            temp1 = (idx_mod & VAR_10) + ((idx_mod >> 1) & VAR_10)
            temp2 = (temp1 & VAR_18) + ((temp1 >> 2) & VAR_18)
            
            current = result[i]
            value = current - VAR_1
            offset = (temp2 & VAR_20) + ((temp2 >> 4) & VAR_20)
            value = (value - offset) % 26
            result[i] = VAR_1 + value
    
    return result

deobfuscated = reverse_obfuscation(normalized, 2)
print(f"After reverse obfuscation: {deobfuscated.decode('ascii')}")
