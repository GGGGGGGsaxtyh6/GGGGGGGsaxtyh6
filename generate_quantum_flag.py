#!/usr/bin/env python3
"""
Generate encrypted flag parts for QUANTUM_ENTANGLEMENT_ULTIMATE
"""

import math

def quantum_encrypt_layer_1(data, key):
    """Layer 1: XOR with rotating key"""
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> ((i % 4) * 8)) & 0xFF))
    return bytes(result)

def quantum_encrypt_layer_2(data, key):
    """Layer 2: Addition with key"""
    result = []
    for i, byte in enumerate(data):
        result.append((byte + (key & 0xFF)) % 256)
    return bytes(result)

def quantum_encrypt_layer_3(data, key):
    """Layer 3: XOR with key bytes"""
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> 8) & 0xFF) ^ ((key >> 16) & 0xFF) ^ ((key >> 24) & 0xFF))
    return bytes(result)

def quantum_encrypt_layer_4(data, key):
    """Layer 4: Multiplication with key"""
    result = []
    for i, byte in enumerate(data):
        result.append((byte * (key & 0xFF)) % 256)
    return bytes(result)

def quantum_encrypt_layer_5(data, key):
    """Layer 5: Complex XOR with key bytes"""
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> 4) & 0xFF) ^ ((key >> 12) & 0xFF) ^ ((key >> 20) & 0xFF) ^ ((key >> 28) & 0xFF))
    return bytes(result)

def quantum_encrypt_layer_6(data, key):
    """Layer 6: Addition with key shift"""
    result = []
    for i, byte in enumerate(data):
        result.append((byte + (key >> 16)) % 256)
    return bytes(result)

def quantum_encrypt_layer_7(data, key):
    """Layer 7: Final XOR"""
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> 24) & 0xFF) ^ ((key >> 8) & 0xFF) ^ ((key >> 0) & 0xFF))
    return bytes(result)

def main():
    # New realistic hacker flag: HTB{QUANTUM_ENTANGLEMENT_BREAKS_ALL_LOCKS}
    flag = "HTB{QUANTUM_ENTANGLEMENT_BREAKS_ALL_LOCKS}"
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
        # Use quantum entanglement weights as decryption keys (same as in C code)
        key = int(math.sin(i * 0.5) * 1000000)
        if key == 0: key = 0x12345678  # Fix for first part
        print(f"Part {i+1} key: 0x{key:08X}")
        
        # Apply all seven quantum encryption layers
        encrypted = quantum_encrypt_layer_7(bytes(part, 'ascii'), key)
        encrypted = quantum_encrypt_layer_6(encrypted, key)
        encrypted = quantum_encrypt_layer_5(encrypted, key)
        encrypted = quantum_encrypt_layer_4(encrypted, key)
        encrypted = quantum_encrypt_layer_3(encrypted, key)
        encrypted = quantum_encrypt_layer_2(encrypted, key)
        encrypted = quantum_encrypt_layer_1(encrypted, key)
        
        encrypted_parts.append(encrypted)
        
        # Print as C array
        hex_values = [f"0x{b:02x}" for b in encrypted]
        print(f"Encrypted part {i+1}: {{{', '.join(hex_values)}}}")
        print()
    
    print("C array for quantum_entanglement.c:")
    print("uint8_t flag_parts[8][16] = {")
    for i, encrypted in enumerate(encrypted_parts):
        hex_values = [f"0x{b:02x}" for b in encrypted]
        print(f"    {{{', '.join(hex_values)}}},")
    print("};")
    
    return encrypted_parts

if __name__ == "__main__":
    main()