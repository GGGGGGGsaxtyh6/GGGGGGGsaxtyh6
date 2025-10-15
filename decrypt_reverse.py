#!/usr/bin/env python3

import struct

# Read config.bin
with open('/workspace/config.bin', 'rb') as f:
    data = f.read()

# Parse file structure
length = struct.unpack('<I', data[0:4])[0]
encrypted_data = bytearray(data[4:4+length])
key_offset = 4 + length + 1
xor_key = bytearray(data[key_offset:])

print(f"Flag length: {length}")
print(f"Encrypted data: {encrypted_data.decode('ascii')}")
print(f"XOR key: {xor_key.hex()}\n")

def reverse_obfuscation(data, iterations):
    """Reverse the obfuscation by subtracting instead of adding"""
    result = bytearray(data)
    
    VAR_10 = 0x55
    VAR_18 = 0x33
    VAR_20 = 0x0F
    VAR_1 = ord('a')
    
    # Apply in reverse order
    for iteration in range(iterations):
        for i in range(len(result)):
            idx_mod = i % 0xFF
            temp1 = (idx_mod & VAR_10) + ((idx_mod >> 1) & VAR_10)
            temp2 = (temp1 & VAR_18) + ((temp1 >> 2) & VAR_18)
            
            current_char = result[i]
            value = current_char - VAR_1
            offset = (temp2 & VAR_20) + ((temp2 >> 4) & VAR_20)
            # Reverse: subtract instead of add
            value = (value - offset) % 26
            result[i] = VAR_1 + value
    
    return result

def xor_buffers(buf1, buf2):
    """XOR two buffers (XOR is its own inverse)"""
    result = bytearray(buf1)
    for i in range(min(len(result), len(buf2))):
        result[i] ^= buf2[i]
    return result

# Try to decrypt: reverse the encryption process
print("=== Attempt 1: Reverse order (XOR first, then deobfuscate) ===\n")

# Step 1: XOR encrypted data with key
after_xor = xor_buffers(encrypted_data, xor_key)
print(f"After XOR: {after_xor.hex()}")

# Filter to only lowercase letters for deobfuscation
normalized = bytearray()
for b in after_xor[:length]:  # Only use first 'length' bytes
    if ord('a') <= b <= ord('z'):
        normalized.append(b)
    else:
        # Map non-letters to letter range
        normalized.append(ord('a') + (b % 26))

print(f"Normalized: {normalized.decode('ascii')}")

# Step 2: Reverse obfuscation
for iterations in [1, 2, 3, 4]:
    result = reverse_obfuscation(normalized, iterations)
    decoded = result.decode('ascii')
    print(f"After reverse obfuscation ({iterations} iterations): {decoded}")
    if 'pico' in decoded.lower() or 'ctf' in decoded.lower():
        print(f"  ^^^ POTENTIAL MATCH!")

print("\n=== Attempt 2: Direct reverse (deobfuscate first, then XOR) ===\n")

# Step 1: Reverse obfuscation on encrypted data
for iterations in [1, 2, 3, 4]:
    deobfuscated = reverse_obfuscation(encrypted_data, iterations)
    print(f"After reverse obfuscation ({iterations} iterations): {deobfuscated.decode('ascii')}")
    
    # Step 2: XOR with key
    result = xor_buffers(deobfuscated, xor_key)
    
    # Try to decode
    printable = ''.join([chr(b) if 32 <= b < 127 else f'\\x{b:02x}' for b in result[:40]])
    print(f"  After XOR: {printable}")
    
    # Try UTF-16-LE
    try:
        flag = result[:40].decode('utf-16-le', errors='ignore')
        print(f"  UTF-16-LE: {flag}")
        if 'pico' in flag.lower() or 'CTF' in flag:
            print(f"    ^^^ POTENTIAL MATCH!")
    except:
        pass
    print()
