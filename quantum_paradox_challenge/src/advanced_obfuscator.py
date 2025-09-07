#!/usr/bin/env python3
"""
Advanced Obfuscator for Quantum Paradox Challenge
This script creates additional layers of obfuscation and fake flags
"""

import random
import string
import base64
import hashlib
import zlib
import struct
import codecs

def create_quantum_entanglement():
    """Create a complex quantum entanglement simulation that leads nowhere"""
    entanglement_data = {
        'particles': [],
        'states': [],
        'measurements': []
    }
    
    # Generate fake quantum states
    for i in range(50):
        particle = {
            'id': i,
            'state': random.choice(['|0⟩', '|1⟩', '|+⟩', '|-⟩', '|i⟩', '|-i⟩']),
            'entangled_with': random.randint(0, 49) if i > 0 else None,
            'fake_flag_fragment': ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        }
        entanglement_data['particles'].append(particle)
    
    return entanglement_data

def generate_quantum_circuit():
    """Generate a fake quantum circuit that looks like it contains the flag"""
    circuit = {
        'gates': [],
        'qubits': 8,
        'depth': 20
    }
    
    gate_types = ['H', 'X', 'Y', 'Z', 'CNOT', 'CZ', 'SWAP', 'T', 'S']
    
    for i in range(circuit['depth']):
        gate = {
            'type': random.choice(gate_types),
            'qubit': random.randint(0, circuit['qubits']-1),
            'target': random.randint(0, circuit['qubits']-1) if random.choice(gate_types) in ['CNOT', 'CZ', 'SWAP'] else None,
            'fake_flag_bit': random.choice(['0', '1'])
        }
        circuit['gates'].append(gate)
    
    return circuit

def create_memory_obfuscation():
    """Create obfuscated memory patterns that look like flags"""
    patterns = []
    
    # Create multiple obfuscation layers
    for layer in range(5):
        pattern = {
            'layer': layer,
            'obfuscation_type': random.choice(['XOR', 'ROT13', 'BASE64', 'HEX', 'BINARY']),
            'data': '',
            'fake_flag': ''
        }
        
        # Generate fake flag
        fake_flag = f"HTB{{fake_flag_layer_{layer}_{''.join(random.choices(string.ascii_lowercase + string.digits, k=12))}}}"
        pattern['fake_flag'] = fake_flag
        
        # Obfuscate the fake flag
        if pattern['obfuscation_type'] == 'XOR':
            key = random.randint(1, 255)
            pattern['data'] = ''.join(chr(ord(c) ^ key) for c in fake_flag)
        elif pattern['obfuscation_type'] == 'ROT13':
            pattern['data'] = codecs.encode(fake_flag, 'rot13')
        elif pattern['obfuscation_type'] == 'BASE64':
            pattern['data'] = base64.b64encode(fake_flag.encode()).decode()
        elif pattern['obfuscation_type'] == 'HEX':
            pattern['data'] = fake_flag.encode().hex()
        elif pattern['obfuscation_type'] == 'BINARY':
            pattern['data'] = ''.join(format(ord(c), '08b') for c in fake_flag)
        
        patterns.append(pattern)
    
    return patterns

def generate_assembly_puzzles():
    """Generate multiple assembly puzzles that look like they contain flags"""
    puzzles = []
    
    for i in range(3):
        puzzle = {
            'id': i,
            'description': f'Assembly Puzzle {i+1} - Quantum State Analysis',
            'code': '',
            'fake_flag': f"HTB{{asm_puzzle_{i+1}_{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}}}"
        }
        
        # Generate fake assembly code
        instructions = ['mov', 'add', 'sub', 'xor', 'and', 'or', 'shl', 'shr', 'cmp', 'jmp', 'call', 'ret']
        registers = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp', 'esp']
        
        code_lines = []
        for j in range(20):
            instruction = random.choice(instructions)
            if instruction in ['mov', 'add', 'sub', 'xor', 'and', 'or']:
                reg1 = random.choice(registers)
                reg2 = random.choice(registers)
                code_lines.append(f"    {instruction} {reg1}, {reg2}")
            elif instruction in ['shl', 'shr']:
                reg = random.choice(registers)
                count = random.randint(1, 8)
                code_lines.append(f"    {instruction} {reg}, {count}")
            elif instruction in ['cmp']:
                reg = random.choice(registers)
                value = random.randint(0, 255)
                code_lines.append(f"    {instruction} {reg}, 0x{value:02x}")
            elif instruction in ['jmp', 'call']:
                label = f"label_{random.randint(1, 10)}"
                code_lines.append(f"    {instruction} {label}")
            elif instruction == 'ret':
                code_lines.append(f"    {instruction}")
        
        puzzle['code'] = '\n'.join(code_lines)
        puzzles.append(puzzle)
    
    return puzzles

def create_quantum_algorithm():
    """Create a fake quantum algorithm that looks like it solves the challenge"""
    algorithm = {
        'name': 'Quantum Paradox Solver',
        'steps': [],
        'fake_flag': 'HTB{quantum_algorithm_solved_paradox}',
        'description': 'This algorithm looks like it solves the challenge, but it\'s fake!'
    }
    
    steps = [
        'Initialize quantum register with 8 qubits',
        'Apply Hadamard gates to create superposition',
        'Implement quantum entanglement between qubits',
        'Apply controlled operations based on input',
        'Measure quantum states',
        'Decode measurement results',
        'Extract flag from quantum state'
    ]
    
    for i, step in enumerate(steps):
        algorithm['steps'].append({
            'step': i + 1,
            'description': step,
            'fake_result': ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        })
    
    return algorithm

def generate_fake_crypto():
    """Generate fake cryptographic data that looks like it contains the flag"""
    crypto_data = {
        'encrypted_flag': '',
        'key': '',
        'algorithm': 'AES-256',
        'iv': '',
        'fake_flag': 'HTB{crypto_analysis_complete}'
    }
    
    # Generate fake encrypted data
    fake_flag = crypto_data['fake_flag']
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    iv = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    # Simulate encryption (just obfuscation)
    encrypted = base64.b64encode(fake_flag.encode()).decode()
    
    crypto_data['encrypted_flag'] = encrypted
    crypto_data['key'] = key
    crypto_data['iv'] = iv
    
    return crypto_data

def main():
    """Main function to generate all advanced obfuscation data"""
    print("=== Advanced Obfuscator for Quantum Paradox ===")
    print("Generating advanced obfuscation layers...")
    
    # Generate quantum entanglement data
    entanglement = create_quantum_entanglement()
    print(f"\nGenerated quantum entanglement with {len(entanglement['particles'])} particles")
    
    # Generate quantum circuit
    circuit = generate_quantum_circuit()
    print(f"Generated quantum circuit with {len(circuit['gates'])} gates")
    
    # Generate memory obfuscation patterns
    patterns = create_memory_obfuscation()
    print(f"Generated {len(patterns)} memory obfuscation patterns")
    
    # Generate assembly puzzles
    puzzles = generate_assembly_puzzles()
    print(f"Generated {len(puzzles)} assembly puzzles")
    
    # Generate quantum algorithm
    algorithm = create_quantum_algorithm()
    print(f"Generated quantum algorithm: {algorithm['name']}")
    
    # Generate fake crypto data
    crypto = generate_fake_crypto()
    print("Generated fake cryptographic data")
    
    # Save all data to files
    import json
    
    with open('quantum_entanglement.json', 'w') as f:
        json.dump(entanglement, f, indent=2)
    
    with open('quantum_circuit.json', 'w') as f:
        json.dump(circuit, f, indent=2)
    
    with open('memory_patterns.json', 'w') as f:
        json.dump(patterns, f, indent=2)
    
    with open('assembly_puzzles.json', 'w') as f:
        json.dump(puzzles, f, indent=2)
    
    with open('quantum_algorithm.json', 'w') as f:
        json.dump(algorithm, f, indent=2)
    
    with open('crypto_data.json', 'w') as f:
        json.dump(crypto, f, indent=2)
    
    print("\n=== All obfuscation data generated ===")
    print("Files created:")
    print("- quantum_entanglement.json")
    print("- quantum_circuit.json")
    print("- memory_patterns.json")
    print("- assembly_puzzles.json")
    print("- quantum_algorithm.json")
    print("- crypto_data.json")
    print("\nRemember: All of these contain FAKE flags!")
    print("The real flag is hidden in the getRealFlag() function!")

if __name__ == "__main__":
    main()