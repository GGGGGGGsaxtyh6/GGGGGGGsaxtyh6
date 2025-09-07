#!/usr/bin/env python3
"""
Quantum Paradox Flag Generator
This script generates multiple fake flags and obfuscates the real one
"""

import random
import string
import base64
import hashlib
import os

def generate_fake_flag(flag_num):
    """Generate a convincing fake flag"""
    prefixes = ["HTB{", "CTF{", "FLAG{", "QUANTUM{"]
    suffixes = ["}", "}", "}", "}"]
    
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    
    # Generate random content
    content_length = random.randint(20, 40)
    content = ''.join(random.choices(string.ascii_lowercase + string.digits + '_', k=content_length))
    
    return f"{prefix}{content}{suffix}"

def obfuscate_string(text, key=0x42):
    """Obfuscate a string using XOR"""
    return ''.join(chr(ord(c) ^ key) for c in text)

def create_fake_binary_data():
    """Create fake binary data that looks like it contains flags"""
    fake_data = []
    
    # Generate multiple fake flags
    for i in range(10):
        fake_flag = generate_fake_flag(i)
        obfuscated = obfuscate_string(fake_flag)
        fake_data.append({
            'original': fake_flag,
            'obfuscated': obfuscated,
            'base64': base64.b64encode(obfuscated.encode()).decode(),
            'md5': hashlib.md5(fake_flag.encode()).hexdigest()
        })
    
    return fake_data

def create_quantum_puzzle():
    """Create a complex puzzle that leads to a fake flag"""
    puzzle = {
        'description': 'Solve the quantum entanglement equation',
        'equation': 'ψ(x,t) = A * e^(i(kx - ωt))',
        'hint': 'The flag is hidden in the imaginary part',
        'fake_solution': 'HTB{qu4ntum_3nt4ngl3m3nt_s0lv3d}',
        'real_hint': 'This is not the real flag - keep looking deeper'
    }
    return puzzle

def generate_memory_patterns():
    """Generate patterns that look like they contain flags in memory"""
    patterns = []
    
    # Create patterns that look like obfuscated flags
    for i in range(5):
        pattern = {
            'address': f"0x{random.randint(0x400000, 0x7fffffff):08x}",
            'data': ''.join(f"{random.randint(0, 255):02x}" for _ in range(32)),
            'description': f'Memory pattern {i+1} - looks like obfuscated flag',
            'fake_flag': generate_fake_flag(i)
        }
        patterns.append(pattern)
    
    return patterns

def create_assembly_puzzle():
    """Create assembly code that looks like it contains the flag"""
    assembly_code = """
    ; Quantum Paradox Assembly Puzzle
    ; This looks like it contains the flag, but it's a decoy
    
    section .text
    global _start
    
    _start:
        mov eax, 0x4854427b    ; "HTB{"
        mov ebx, 0x66616b33    ; "fak3"
        mov ecx, 0x5f666c34    ; "_fl4"
        mov edx, 0x675f6173    ; "g_as"
        mov esi, 0x73656d62    ; "semb"
        mov edi, 0x6c795f6c    ; "ly_l"
        mov ebp, 0x6f6f6b73    ; "ooks"
        mov esp, 0x5f6c696b    ; "_lik"
        mov eax, 0x655f666c    ; "e_fl"
        mov ebx, 0x61675f62    ; "ag_b"
        mov ecx, 0x75745f69    ; "ut_i"
        mov edx, 0x735f6e6f    ; "s_no"
        mov esi, 0x745f7468    ; "t_th"
        mov edi, 0x655f7265    ; "e_re"
        mov ebp, 0x616c5f66    ; "al_f"
        mov esp, 0x6c61677d    ; "lag}"
        
        ; This is just a decoy - the real flag is elsewhere
        int 0x80
    """
    
    return assembly_code

def main():
    """Main function to generate all fake data"""
    print("=== Quantum Paradox Flag Generator ===")
    print("Generating fake flags and puzzles...")
    
    # Generate fake binary data
    fake_data = create_fake_binary_data()
    print(f"\nGenerated {len(fake_data)} fake flags:")
    for i, data in enumerate(fake_data):
        print(f"Fake Flag {i+1}: {data['original']}")
        print(f"  Obfuscated: {data['obfuscated']}")
        print(f"  Base64: {data['base64']}")
        print(f"  MD5: {data['md5']}")
        print()
    
    # Generate quantum puzzle
    puzzle = create_quantum_puzzle()
    print("Quantum Puzzle:")
    print(f"Description: {puzzle['description']}")
    print(f"Equation: {puzzle['equation']}")
    print(f"Hint: {puzzle['hint']}")
    print(f"Fake Solution: {puzzle['fake_solution']}")
    print(f"Real Hint: {puzzle['real_hint']}")
    print()
    
    # Generate memory patterns
    patterns = generate_memory_patterns()
    print("Memory Patterns (fake flags):")
    for pattern in patterns:
        print(f"Address: {pattern['address']}")
        print(f"Data: {pattern['data']}")
        print(f"Description: {pattern['description']}")
        print(f"Fake Flag: {pattern['fake_flag']}")
        print()
    
    # Generate assembly puzzle
    assembly = create_assembly_puzzle()
    print("Assembly Puzzle (decoy):")
    print(assembly)
    
    print("\n=== All fake data generated ===")
    print("Remember: The real flag is hidden much deeper in the binary!")
    print("Look for the getRealFlag() function and analyze memory dumps carefully.")

if __name__ == "__main__":
    main()