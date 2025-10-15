#!/usr/bin/env python3

import struct

# Read config.bin
with open('/workspace/config.bin', 'rb') as f:
    data = f.read()

# Parse file structure correctly
length = struct.unpack('<I', data[0:4])[0]
print(f"Flag length: {length}")

# Encrypted data: offset 4 to 4+length
encrypted_data = bytearray(data[4:4+length])
print(f"Encrypted data: {encrypted_data.decode('ascii')}")

# XOR key: starts at offset 4+length+1 (skipping the 0x00 byte separator)
key_offset = 4 + length + 1
xor_key = bytearray(data[key_offset:])
print(f"XOR key ({len(xor_key)} bytes): {xor_key.hex()}")

def obfuscate_data(data, iterations):
    """Implements fcn.0040122b"""
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
            
            current_char = result[i]
            value = current_char - VAR_1
            offset = (temp2 & VAR_20) + ((temp2 >> 4) & VAR_20)
            value = (value + offset) % 26
            result[i] = VAR_1 + value
    
    return result

def xor_buffers(key_buffer, data_buffer):
    """Implements fcn.0040127b - XORs key with data"""
    result = bytearray(key_buffer)
    for i in range(min(len(result), len(data_buffer))):
        result[i] ^= data_buffer[i]
    return result

# Simulate the flag generation process
print("\n=== Flag Generation Simulation ===\n")

# Step 1: Apply obfuscation to encrypted data (2 iterations)
obfuscated = obfuscate_data(encrypted_data, 2)
print(f"Step 1 - After obfuscation:")
print(f"  {obfuscated.decode('ascii')}")

# Step 2: XOR the key with obfuscated data
final_result = xor_buffers(xor_key, obfuscated)
print(f"\nStep 2 - After XOR:")
print(f"  Hex: {final_result.hex()}")

# Decode as UTF-16-LE
print(f"\n=== Final Result ===")
try:
    flag_utf16 = final_result.decode('utf-16-le', errors='strict')
    print(f"UTF-16-LE: {flag_utf16}")
except Exception as e:
    print(f"UTF-16-LE decode error: {e}")
    # Try with errors='ignore'
    flag_utf16 = final_result.decode('utf-16-le', errors='ignore')
    print(f"UTF-16-LE (ignore errors): {flag_utf16}")

# Also try as ASCII
printable = ''.join([chr(b) if 32 <= b < 127 else f'\\x{b:02x}' for b in final_result])
print(f"ASCII representation: {printable}")

# Extract only printable ASCII characters
printable_only = ''.join([chr(b) for b in final_result if 32 <= b < 127])
print(f"Printable chars only: {printable_only}")
