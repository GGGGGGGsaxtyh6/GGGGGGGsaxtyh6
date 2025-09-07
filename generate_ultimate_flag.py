#!/usr/bin/env python3
"""
Flag generator for NEURAL_CORRUPTION_ULTIMATE challenge
This generates the correct flag with proper encryption
"""

import math

# Neural weights (same as in C code)
neural_weights = [
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
    [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
    [0.2, 0.4, 0.6, 0.8, 0.1, 0.3, 0.5, 0.7],
    [0.7, 0.5, 0.3, 0.1, 0.8, 0.6, 0.4, 0.2],
    [0.3, 0.6, 0.1, 0.4, 0.7, 0.2, 0.5, 0.8],
    [0.8, 0.5, 0.2, 0.7, 0.4, 0.1, 0.6, 0.3],
    [0.4, 0.8, 0.2, 0.6, 0.1, 0.5, 0.3, 0.7],
    [0.7, 0.3, 0.5, 0.1, 0.6, 0.2, 0.8, 0.4]
]

def encrypt_layer_1(data, key):
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> ((i % 4) * 8)) & 0xFF))
    return bytes(result)

def encrypt_layer_2(data, key):
    result = []
    for i, byte in enumerate(data):
        result.append((byte + (key & 0xFF)) % 256)
    return bytes(result)

def encrypt_layer_3(data, key):
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> 8) & 0xFF) ^ ((key >> 16) & 0xFF) ^ ((key >> 24) & 0xFF))
    return bytes(result)

def main():
    # The real flag
    full_flag = b"HTB{NEURAL_CORRUPTION_ULTIMATE_IS_THE_MOST_INSANE_RETO_EVER_CREATED_BY_THE_AI_MASTER_OF_THE_NEURAL_NETWORK_AND_THE_CORRUPTED_VM_BYTECODE_ANALYSIS_MASTER_WHO_BROKE_THE_NEURAL_NETWORK_AND_THE_CORRUPTED_VM_BYTECODE_ANALYSIS_MASTER_OF_THE_ULTIMATE_RETO_CHALLENGE}"
    
    # Split into 8 parts
    part_size = len(full_flag) // 8
    flag_parts = []
    
    for i in range(8):
        start = i * part_size
        if i == 7:  # Last part gets the remainder
            end = len(full_flag)
        else:
            end = start + part_size
        flag_parts.append(full_flag[start:end])
    
    print("Real flag parts:")
    for i, part in enumerate(flag_parts):
        print(f"Part {i}: {part}")
    
    print("\nEncrypted flag parts (hex):")
    for i, part in enumerate(flag_parts):
        # Use neural weights as encryption keys
        key = int(neural_weights[i][0] * 1000000)
        
        # Apply all three encryption layers
        encrypted = encrypt_layer_1(part, key)
        encrypted = encrypt_layer_2(encrypted, key)
        encrypted = encrypt_layer_3(encrypted, key)
        
        print(f"Part {i}: {[hex(b) for b in encrypted]}")
    
    print(f"\nFull flag: {full_flag.decode()}")

if __name__ == "__main__":
    main()