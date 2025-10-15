#!/usr/bin/env python3
import struct
import subprocess

class TinyVMEmulator:
    def __init__(self):
        self.stack = []
        self.regs = [0, 0, 0]  # 3 registers
        self.pc = 0
        
    def push(self, value):
        self.stack.append(value & 0xFFFF)
        
    def pop(self):
        if not self.stack:
            return 0
        return self.stack.pop()
    
    def peek(self):
        if not self.stack:
            return 0
        return self.stack[-1]
    
    def execute_instruction(self, instr):
        opcode = (instr >> 16) & 0xFF
        operand = instr & 0xFFFF
        operand_byte = instr & 0xFF
        
        if opcode == 0:  # PUSH immediate
            self.push(operand)
        elif opcode == 1:  # PUSH from register
            if operand_byte < 3:
                self.push(self.regs[operand_byte])
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
        elif opcode == 8:  # ROT (rotate top 3)
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

# Load bytecode
with open('tiny_vm', 'rb') as f:
    data = f.read()

file_offset = 0x690c0
bytecode_bytes = data[file_offset:file_offset+10457*4]
bytecode = [struct.unpack('<I', bytecode_bytes[i*4:i*4+4])[0] for i in range(10457)]

expected_output = bytes([129, 162, 253, 190, 189, 69, 44, 25, 242, 51, 201, 199, 165, 240, 188, 73, 222, 136, 182, 219, 17, 206, 31, 35, 252, 185])

# Intento 1: Buscar en el bytecode secuencias que parezcan ser la flag
print("=== Buscando patrones en el bytecode ===")

# Extraer todos los valores PUSH
all_push_values = []
for i in range(len(bytecode)):
    instr = bytecode[i]
    opcode = (instr >> 16) & 0xFF
    operand = instr & 0xFFFF
    if opcode == 0:
        all_push_values.append((i, operand))

# Buscar secuencias que empiecen con 'i' (0x69), 'c' (0x63), 't' (0x74), 'f' (0x66)
print("\nBuscando secuencia 'ictf{' en valores PUSH:")
for i in range(len(all_push_values) - 5):
    vals = [all_push_values[i+j][1] for j in range(5)]
    if vals[0] == ord('i') and vals[1] == ord('c') and vals[2] == ord('t') and vals[3] == ord('f') and vals[4] == ord('{'):
        print(f"  Encontrado en posición {i}!")
        # Extraer los siguientes 26 valores
        flag_chars = []
        for j in range(26):
            if i+j < len(all_push_values):
                val = all_push_values[i+j][1]
                if val < 256:
                    flag_chars.append(chr(val))
        if len(flag_chars) == 26:
            candidate = ''.join(flag_chars)
            print(f"  Candidato: {candidate}")
            # Probar
            with open('/tmp/test.txt', 'w') as f:
                f.write(candidate)
            proc = subprocess.run(['./tiny_vm'], stdin=open('/tmp/test.txt'), 
                                capture_output=True, text=True, timeout=2)
            if "Correct" in proc.stdout:
                print(f"\n🎉🎉🎉 FLAG ENCONTRADA: {candidate} 🎉🎉🎉\n")
                with open('/workspace/FLAG.txt', 'w') as f:
                    f.write(candidate)
                exit(0)

print("\n=== Intento 2: Análisis del patrón XOR más detallado ===")

# El patrón que vi antes: posiciones impares tienen "Mkey!tinyVMkey!..."
# Posiciones pares tienen contadores
# Voy a probar diferentes offsets y operaciones

for start in range(20, 40):
    for operation in ['xor', 'add', 'sub']:
        chars = []
        for i in range(start, min(start + 52, len(all_push_values)), 2):
            if i+1 < len(all_push_values):
                val1 = all_push_values[i][1]
                val2 = all_push_values[i+1][1]
                
                if operation == 'xor':
                    result = val1 ^ val2
                elif operation == 'add':
                    result = (val1 + val2) & 0xFF
                else:  # sub
                    result = (val1 - val2) & 0xFF
                
                if 0 <= result < 256:
                    chars.append(result)
        
        if len(chars) >= 26:
            flag_bytes = bytes(chars[:26])
            try:
                flag = flag_bytes.decode('ascii')
                if flag.startswith('ictf{') or 'ictf' in flag:
                    print(f"Candidato (start={start}, op={operation}): {flag}")
                    with open('/tmp/test.txt', 'w') as f:
                        f.write(flag)
                    proc = subprocess.run(['./tiny_vm'], stdin=open('/tmp/test.txt'), 
                                        capture_output=True, text=True, timeout=2)
                    if "Correct" in proc.stdout:
                        print(f"\n🎉 FLAG: {flag} 🎉\n")
                        with open('/workspace/FLAG.txt', 'w') as f:
                            f.write(flag)
                        exit(0)
            except:
                pass

print("\n=== Intento 3: Probar con el output esperado ===")
# Tal vez el output esperado ES la flag o está relacionado
print(f"Output esperado: {expected_output}")
print(f"Como ASCII: {expected_output.decode('ascii', errors='replace')}")

# Probar XOR del output con "tinyVMkey!" repetido
key = b'tinyVMkey!' * 3
key = key[:26]
flag_from_output = bytes([expected_output[i] ^ key[i] for i in range(26)])
try:
    flag_str = flag_from_output.decode('ascii')
    print(f"Output XOR tinyVMkey: {flag_str}")
    with open('/tmp/test.txt', 'w') as f:
        f.write(flag_str)
    proc = subprocess.run(['./tiny_vm'], stdin=open('/tmp/test.txt'), 
                        capture_output=True, text=True, timeout=2)
    if "Correct" in proc.stdout:
        print(f"\n🎉 FLAG: {flag_str} 🎉\n")
        with open('/workspace/FLAG.txt', 'w') as f:
            f.write(flag_str)
        exit(0)
except:
    pass

print("\nContinuando con más intentos...")
