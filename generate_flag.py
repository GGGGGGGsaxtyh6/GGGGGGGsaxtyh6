#!/usr/bin/env python3
"""
Flag generator for NEURAL_CORRUPTION challenge
This generates the correct flag parts with proper encryption
"""

import math

# Neural constants (same as in the C code)
NEURAL_CONSTANTS = [
    3.141592653589793, 2.718281828459045, 1.414213562373095,
    1.732050807568877, 2.236067977499790, 2.645751311064591,
    3.162277660168379, 2.828427124746190
]

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def neural_encrypt(data, key):
    """Encrypt data using neural network algorithm"""
    result = []
    for i, byte in enumerate(data):
        neural_val = sigmoid(key * (i + 1) / 256.0)
        encrypted_byte = byte ^ int(neural_val * 255)
        result.append(encrypted_byte)
        key = key * 1.618033988749895  # Golden ratio
    return bytes(result)

def main():
    # The real flag parts
    flag_parts = [
        b"HTB{NEURAL_CORRUPTION_IS_REAL_NOT_MORE_FAKE_RETOS_FROM_THE_AI_MASTER_OF_THE_NEURAL_NETWORK_AND_THE_CORRUPTED_VM_BYTECODE_ANALYSIS_MASTER}",
        b"",  # Empty parts to confuse
        b"",
        b"",
        b"",
        b"",
        b"",
        b""
    ]
    
    # Split the flag into 8 parts
    full_flag = flag_parts[0]
    part_size = len(full_flag) // 8
    real_parts = []
    
    for i in range(8):
        start = i * part_size
        if i == 7:  # Last part gets the remainder
            end = len(full_flag)
        else:
            end = start + part_size
        real_parts.append(full_flag[start:end])
    
    print("Real flag parts:")
    for i, part in enumerate(real_parts):
        print(f"Part {i}: {part}")
    
    print("\nEncrypted flag parts (hex):")
    for i, part in enumerate(real_parts):
        if len(part) > 0:
            # Use neural constant as key
            key = NEURAL_CONSTANTS[i] * 1000000 / 1000000.0  # Simulate register value
            encrypted = neural_encrypt(part, key)
            print(f"Part {i}: {[hex(b) for b in encrypted]}")
    
    print(f"\nFull flag: {full_flag.decode()}")

if __name__ == "__main__":
    main()