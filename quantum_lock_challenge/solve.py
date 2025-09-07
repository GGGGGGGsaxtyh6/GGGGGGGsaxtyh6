#!/usr/bin/env python3
"""
QUANTUM_LOCK Challenge Solver

This script solves the QUANTUM_LOCK challenge by:
1. Deriving quantum keys from entangled register pairs
2. Decrypting the flag parts using the derived keys
3. Reconstructing the complete flag

Author: AI Assistant
"""

# Quantum constants loaded into registers 0-7
constants = [
    0xDEADBEEF, 0xCAFEBABE, 0xFEEDFACE, 0xBADDCAFE,
    0x1337C0DE, 0xDEADC0DE, 0xFEEDBEEF, 0xCAFEDEAD
]

def derive_quantum_keys():
    """Derive quantum keys from entangled register pairs"""
    keys = [
        constants[0] ^ constants[1],  # reg0 ^ reg1
        constants[2] ^ constants[3],  # reg2 ^ reg3
        constants[4] ^ constants[5],  # reg4 ^ reg5
        constants[6] ^ constants[7]   # reg6 ^ reg7
    ]
    return keys

def decrypt_part(data, key):
    """Decrypt a flag part using XOR with rotating key"""
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> ((i % 4) * 8)) & 0xFF))
    return bytes(result)

def main():
    print("=== QUANTUM_LOCK Challenge Solver ===")
    print()
    
    # Encrypted flag parts (extracted from the binary)
    flag_parts = [
        [0x19, 0x50, 0x11, 0x6F, 0x00, 0x51, 0x12, 0x5A, 0x05, 0x51, 0x1E, 0x4B],
        [0x7C, 0x7F, 0x73, 0x0F, 0x6F, 0x79, 0x63, 0x1B, 0x72, 0x62, 0x7F, 0x0F, 0x75, 0x7E],
        [0x5F, 0x42, 0xC3, 0x92, 0x54, 0x48, 0xDF, 0x92, 0x52, 0x45, 0xCC, 0x88, 0x52, 0x53, 0xDF, 0x9F],
        [0x1D, 0x2D, 0x52, 0x67, 0x16, 0x25, 0x41, 0x49]
    ]
    
    # Derive quantum keys
    keys = derive_quantum_keys()
    
    print("Quantum Constants:")
    for i, const in enumerate(constants):
        print(f"  reg{i}: 0x{const:08X}")
    print()
    
    print("Derived Quantum Keys:")
    for i, key in enumerate(keys):
        print(f"  key{i+1}: 0x{key:08X}")
    print()
    
    # Decrypt each flag part
    decrypted_parts = []
    print("Decrypting flag parts:")
    for i, (part, key) in enumerate(zip(flag_parts, keys)):
        decrypted = decrypt_part(part, key)
        decrypted_parts.append(decrypted.decode('ascii'))
        print(f"  Part {i+1}: {decrypted.decode('ascii')}")
    print()
    
    # Reconstruct the complete flag
    flag = ''.join(decrypted_parts)
    print("=== QUANTUM LOCK UNLOCKED! ===")
    print(f"Flag: {flag}")
    print()
    
    # Verify the flag
    expected_flag = "HTB{QUANTUM_LOCK_IS_BROKEN_BY_THE_REVERSER_MASTER}"
    if flag == expected_flag:
        print("✅ Flag verification successful!")
    else:
        print("❌ Flag verification failed!")
        print(f"Expected: {expected_flag}")
        print(f"Got:      {flag}")

if __name__ == "__main__":
    main()