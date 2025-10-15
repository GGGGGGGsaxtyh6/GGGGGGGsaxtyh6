#!/usr/bin/env python3

import struct

# Read config.bin
with open('/workspace/config.bin', 'rb') as f:
    data = f.read()

# Parse config.bin structure
length = struct.unpack('<I', data[0:4])[0]
print(f"Flag length: {length}")

# The encrypted flag data
encrypted_data = bytearray(data[4:4+length])
print(f"Encrypted data: {encrypted_data.decode('ascii')}")

# The XOR key starts right after the encrypted data
xor_key_offset = 4 + length
# Based on the code at 0x402a9b, it checks: read_size == length*2 + 2
expected_key_len = length * 2 + 2
xor_key = bytearray(data[xor_key_offset:xor_key_offset + expected_key_len])
print(f"XOR key length: {len(xor_key)} (expected: {expected_key_len})")
print(f"XOR key (hex): {xor_key.hex()}")

# Based on the assembly analysis:
# 1. The flag data is loaded into memory at [0x40c3d0]
# 2. fcn.0040122b is called with arg 2 at 0x4037b8
# 3. fcn.0040127b is called with the flag pointer at 0x4038f1
# 4. The final result is in the XOR key buffer at [0x40c3d4]

def obfuscate_data(data, iterations):
    """
    Implements fcn.0040122b at 0x402bc0
    This function obfuscates the data based on position
    """
    result = bytearray(data)
    
    VAR_10 = 0x55
    VAR_18 = 0x33
    VAR_20 = 0x0F
    VAR_1 = ord('a')
    
    data_len = len(result)
    
    for iteration in range(iterations):
        for i in range(data_len):
            # Calculate index-based offset
            idx_mod = i % 0xFF
            temp1 = (idx_mod & VAR_10) + ((idx_mod >> 1) & VAR_10)
            temp2 = (temp1 & VAR_18) + ((temp1 >> 2) & VAR_18)
            
            # Get current character
            current_char = result[i]
            
            # Apply transformation
            value = current_char - VAR_1
            offset = (temp2 & VAR_20) + ((temp2 >> 4) & VAR_20)
            value = (value + offset) % 26
            result[i] = VAR_1 + value
    
    return result

def xor_buffers(key_buffer, data_buffer):
    """
    Implements fcn.0040127b at 0x402cb0
    XORs key_buffer with data_buffer (modifies key_buffer)
    """
    result = bytearray(key_buffer)
    min_len = min(len(result), len(data_buffer))
    
    for i in range(min_len):
        result[i] ^= data_buffer[i]
    
    return result

# Simulate the process
print("\n=== Simulating flag generation ===")

# Step 1: Copy encrypted data to working buffer (simulating [0x40c3d0])
working_data = bytearray(encrypted_data)

# Step 2: Apply obfuscation with 2 iterations
obfuscated = obfuscate_data(working_data, 2)
print(f"\nAfter obfuscation (2 iterations):")
print(f"  ASCII: {obfuscated.decode('ascii')}")

# Step 3: XOR the key buffer with obfuscated data
# The key buffer starts at [0x40c3d4]
result = xor_buffers(xor_key, obfuscated)
print(f"\nAfter XOR with key:")
print(f"  Hex: {result.hex()}")
print(f"  Raw bytes: {result}")

# Try to decode as UTF-16-LE (wide char string)
print(f"\n=== Attempting UTF-16-LE decode ===")
try:
    flag = result.decode('utf-16-le', errors='ignore')
    print(f"Flag (UTF-16-LE): {flag}")
except Exception as e:
    print(f"Error: {e}")

# Try different interpretations
print(f"\n=== Other interpretations ===")

# As ASCII
ascii_result = ''.join([chr(b) if 32 <= b < 127 else f'\\x{b:02x}' for b in result])
print(f"As ASCII: {ascii_result}")

# Extracting only printable ASCII
printable = ''.join([chr(b) for b in result if 32 <= b < 127])
print(f"Printable only: {printable}")
