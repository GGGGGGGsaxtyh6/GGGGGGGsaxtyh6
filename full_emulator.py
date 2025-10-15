#!/usr/bin/env python3
import struct
import subprocess
from multiprocessing import Pool, cpu_count
import string

# Cargar bytecode
with open('tiny_vm', 'rb') as f:
    data = f.read()

file_offset = 0x690c0
bytecode_bytes = data[file_offset:file_offset+10457*4]
bytecode = [struct.unpack('<I', bytecode_bytes[i*4:i*4+4])[0] for i in range(10457)]

expected_output = bytes([129, 162, 253, 190, 189, 69, 44, 25, 242, 51, 201, 199, 165, 240, 188, 73, 222, 136, 182, 219, 17, 206, 31, 35, 252, 185])

class TinyVM:
    def __init__(self, input_str):
        self.stack = []
        self.regs = [0, 0, 0]
        self.input_chars = [ord(c) for c in input_str]
        self.pc = 0
        self.output = []
        
    def push(self, val):
        self.stack.append(val & 0xFFFF)
        
    def pop(self):
        return self.stack.pop() if self.stack else 0
    
    def peek(self):
        return self.stack[-1] if self.stack else 0
    
    def run(self, max_steps=100000):
        for step in range(max_steps):
            if self.pc >= len(bytecode):
                break
                
            instr = bytecode[self.pc]
            opcode = (instr >> 16) & 0xFF
            operand = instr & 0xFFFF
            operand_byte = instr & 0xFF
            
            if opcode == 0:  # PUSH immediate
                self.push(operand)
            elif opcode == 1:  # PUSH from register/input
                if operand_byte < 3:
                    self.push(self.regs[operand_byte])
                elif operand_byte < 26 + 3:  # Input characters
                    idx = operand_byte - 3
                    if idx < len(self.input_chars):
                        self.push(self.input_chars[idx])
                    else:
                        self.push(0)
            elif opcode == 2:  # POP to register
                if operand_byte < 3:
                    self.regs[operand_byte] = self.pop()
            elif opcode == 3:  # ADD
                b = self.pop()
                a = self.pop()
                self.push((a + b) & 0xFFFF)
            elif opcode == 4:  # XOR
                b = self.pop()
                a = self.pop()
                self.push((a ^ b) & 0xFFFF)
            elif opcode == 5:  # SUB
                b = self.pop()
                a = self.pop()
                self.push((a - b) & 0xFFFF)
            elif opcode == 6:  # DUP
                self.push(self.peek())
            elif opcode == 7:  # SWAP
                b = self.pop()
                a = self.pop()
                self.push(b)
                self.push(a)
            elif opcode == 8:  # ROT
                c = self.pop()
                b = self.pop()
                a = self.pop()
                self.push(b)
                self.push(c)
                self.push(a)
            elif opcode == 9:  # OVER
                b = self.pop()
                a = self.peek()
                self.push(b)
                self.push(a)
            elif opcode == 10:  # DROP
                self.pop()
            elif opcode == 11:  # MUL
                b = self.pop()
                a = self.pop()
                self.push((a * b) & 0xFFFF)
            elif opcode == 12:  # EQ
                b = self.pop()
                a = self.pop()
                self.push(1 if a == b else 0)
                
            self.pc += 1
        
        # Extract top 26 values from stack as output
        if len(self.stack) >= 26:
            self.output = [self.stack[-(26-i)] & 0xFF for i in range(26)]
        return bytes(self.output)

def test_with_emulator(flag):
    """Emular y comparar con salida esperada"""
    if len(flag) != 26:
        return False
    try:
        vm = TinyVM(flag)
        output = vm.run()
        return output == expected_output
    except:
        return False

def test_with_binary(flag):
    """Probar con el binario real"""
    if len(flag) != 26:
        return False
    try:
        with open('/tmp/test.txt', 'w') as f:
            f.write(flag)
        proc = subprocess.run(['./tiny_vm'], stdin=open('/tmp/test.txt'), 
                            capture_output=True, text=True, timeout=2)
        return "Correct" in proc.stdout
    except:
        return False

# Generar candidatos basados en patrones
def generate_candidates():
    candidates = []
    
    # Palabras comunes
    words = ['tiny', 'vm', 'stack', 'hidden', 'key', 'flag', 'misplaced',
             'bytecode', 'instr', 'reverse', 'crack', 'pwn', 'found', 'lost']
    
    # Variaciones con leetspeak
    leet_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
    
    for w1 in words:
        for w2 in words:
            if w1 != w2:
                # Variación 1: word1_word2
                middle = f"{w1}_{w2}"
                # Leetspeak
                leet_middle = middle
                for k, v in leet_map.items():
                    leet_middle = leet_middle.replace(k, v)
                
                # Rellenar hasta 20 chars
                for filler in ['!', '_', '@', '#']:
                    for count in range(1, 10):
                        test_middle = leet_middle + filler * count
                        if len(test_middle) == 20:
                            candidates.append(f"ictf{{{test_middle}}}")
    
    return candidates

print("Generando candidatos...")
candidates = generate_candidates()
print(f"Total de candidatos: {len(candidates)}")

print("\nProbando con el binario real (primeros 1000)...")
for i, flag in enumerate(candidates[:1000]):
    if i % 100 == 0:
        print(f"  Progreso: {i}/1000")
    
    if test_with_binary(flag):
        print(f"\n🎉🎉🎉 FLAG ENCONTRADA: {flag} 🎉🎉🎉\n")
        with open('/workspace/FLAG.txt', 'w') as f:
            f.write(flag)
        exit(0)

print("\n⚠️ No encontrado en primeros 1000. Continuando...")
