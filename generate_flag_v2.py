#!/usr/bin/env python3
"""
Generate encrypted flag parts for NEURAL_CORRUPTION_ULTIMATE V2
"""

import math

def encrypt_layer_1(data, key):
    """Layer 1: XOR with rotating key"""
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> ((i % 4) * 8)) & 0xFF))
    return bytes(result)

def encrypt_layer_2(data, key):
    """Layer 2: Addition with key"""
    result = []
    for i, byte in enumerate(data):
        result.append((byte + (key & 0xFF)) % 256)
    return bytes(result)

def encrypt_layer_3(data, key):
    """Layer 3: XOR with key bytes"""
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> 8) & 0xFF) ^ ((key >> 16) & 0xFF) ^ ((key >> 24) & 0xFF))
    return bytes(result)

def encrypt_layer_4(data, key):
    """Layer 4: Multiplication with key"""
    result = []
    for i, byte in enumerate(data):
        result.append((byte * (key & 0xFF)) % 256)
    return bytes(result)

def encrypt_layer_5(data, key):
    """Layer 5: Complex XOR with key bytes"""
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> 4) & 0xFF) ^ ((key >> 12) & 0xFF) ^ ((key >> 20) & 0xFF) ^ ((key >> 28) & 0xFF))
    return bytes(result)

def main():
    # New shorter flag: HTB{NEURAL_CORRUPTION_ULTIMATE_V2_MASTER}
    flag = "HTB{NEURAL_CORRUPTION_ULTIMATE_V2_MASTER}"
    print(f"Original flag: {flag}")
    print(f"Flag length: {len(flag)} characters")
    print()
    
    # Split flag into 8 parts (16 bytes each, padded with nulls)
    flag_parts = []
    for i in range(8):
        start = i * 16
        end = start + 16
        part = flag[start:end].ljust(16, '\x00')
        flag_parts.append(part)
        print(f"Part {i+1}: '{part}' (length: {len(part)})")
    
    print()
    print("Encrypting each part:")
    
    # Encrypt each part
    encrypted_parts = []
    for i, part in enumerate(flag_parts):
        # Use neural weights as decryption keys (same as in C code)
        key = int(math.sin(i * 0.5) * 1000000)
        if key == 0: key = 0x12345678  # Fix for first part
        print(f"Part {i+1} key: 0x{key:08X}")
        
        # Apply all five encryption layers
        encrypted = encrypt_layer_5(bytes(part, 'ascii'), key)
        encrypted = encrypt_layer_4(encrypted, key)
        encrypted = encrypt_layer_3(encrypted, key)
        encrypted = encrypt_layer_2(encrypted, key)
        encrypted = encrypt_layer_1(encrypted, key)
        
        encrypted_parts.append(encrypted)
        
        # Print as C array
        hex_values = [f"0x{b:02x}" for b in encrypted]
        print(f"Encrypted part {i+1}: {{{', '.join(hex_values)}}}")
        print()
    
    print("C array for neural_ultimate_v2.c:")
    print("uint8_t flag_parts[8][16] = {")
    for i, encrypted in enumerate(encrypted_parts):
        hex_values = [f"0x{b:02x}" for b in encrypted]
        print(f"    {{{', '.join(hex_values)}}},")
    print("};")
    
    return encrypted_parts

if __name__ == "__main__":
    main()