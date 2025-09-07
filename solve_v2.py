#!/usr/bin/env python3
"""
NEURAL_CORRUPTION_ULTIMATE V2 Challenge Solver
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
    print("=== NEURAL CORRUPTION ULTIMATE V2 SOLVER ===")
    print()
    
    # Encrypted flag parts from the binary
    flag_parts = [
        [0x50, 0xde, 0xcc, 0x42, 0x20, 0xf6, 0x14, 0x6a, 0xf8, 0x1e, 0x44, 0x82, 0x88, 0x2e, 0x4c, 0x32],
        [0xbe, 0x2b, 0x2f, 0xa2, 0x20, 0xe2, 0x3b, 0x63, 0xba, 0x78, 0x23, 0x30, 0xba, 0x7c, 0xb5, 0xf9],
        [0xc6, 0x0c, 0xfa, 0xde, 0x3c, 0x1a, 0xea, 0xf8, 0x68, 0xb2, 0x68, 0x64, 0x9a, 0xb2, 0x68, 0x64],
        [0xb3, 0xfd, 0xca, 0xc5, 0xb3, 0xfd, 0xca, 0xc5, 0xb3, 0xfd, 0xca, 0xc5, 0xb3, 0xfd, 0xca, 0xc5],
        [0x30, 0x1e, 0xcc, 0xc1, 0x30, 0x1e, 0xcc, 0xc1, 0x30, 0x1e, 0xcc, 0xc1, 0x30, 0x1e, 0xcc, 0xc1],
        [0x68, 0x81, 0xa9, 0xa0, 0x68, 0x81, 0xa9, 0xa0, 0x68, 0x81, 0xa9, 0xa0, 0x68, 0x81, 0xa9, 0xa0],
        [0xa5, 0xc2, 0xe7, 0xe5, 0xa5, 0xc2, 0xe7, 0xe5, 0xa5, 0xc2, 0xe7, 0xe5, 0xa5, 0xc2, 0xe7, 0xe5],
        [0x56, 0x32, 0x6d, 0x68, 0x56, 0x32, 0x6d, 0x68, 0x56, 0x32, 0x6d, 0x68, 0x56, 0x32, 0x6d, 0x68]
    ]
    
    print("Derived Decryption Keys:")
    keys = []
    for i in range(8):
        key = int(math.sin(i * 0.5) * 1000000)
        if key == 0: key = 0x12345678  # Fix for first part
        keys.append(key)
        print(f"  Key {i+1}: 0x{key:08X} (from sin({i} * 0.5) * 1000000)")
    print()
    
    # Decrypt each flag part
    decrypted_parts = []
    print("Decrypting flag parts:")
    for i, part in enumerate(flag_parts):
        key = keys[i]
        
        # Apply all five encryption layers (in reverse order for decryption)
        decrypted = encrypt_layer_5(bytes(part), key)
        decrypted = encrypt_layer_4(decrypted, key)
        decrypted = encrypt_layer_3(decrypted, key)
        decrypted = encrypt_layer_2(decrypted, key)
        decrypted = encrypt_layer_1(decrypted, key)
        
        # Clean up the decrypted string
        clean_string = decrypted.decode('ascii', errors='ignore').rstrip('\x00')
        decrypted_parts.append(clean_string)
        print(f"  Part {i+1}: '{clean_string}'")
    
    # Reconstruct the complete flag
    flag = ''.join(decrypted_parts)
    print()
    print("=== NEURAL CORRUPTION ULTIMATE V2 ANALYZED! ===")
    print(f"Real Flag: {flag}")
    print()
    
    # Verify the flag
    expected_start = "HTB{"
    expected_end = "}"
    if flag.startswith(expected_start) and flag.endswith(expected_end):
        print("✅ Flag verification successful!")
        print(f"Flag length: {len(flag)} characters")
    else:
        print("❌ Flag verification failed!")
        print(f"Expected format: HTB{{...}}")
        print(f"Got: {flag}")
    
    return flag

if __name__ == "__main__":
    main()