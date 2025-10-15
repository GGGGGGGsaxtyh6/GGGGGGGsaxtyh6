#!/usr/bin/env python3
import struct

class TinyVM:
    def __init__(self, input1, input2):
        self.stack = []
        self.regs = [0, 0, 0]
        self.input1 = [ord(c) if isinstance(c, str) else c for c in input1]
        self.input2 = [ord(c) if isinstance(c, str) else c for c in input2]
        self.pc = 0
        
    def push(self, value):
        self.stack.append(value & 0xFFFF)
        
    def pop(self):
        if not self.stack:
            raise Exception("Stack underflow at PC=%d" % self.pc)
        return self.stack.pop()
    
    def peek(self):
        if not self.stack:
            raise Exception("Stack underflow (peek) at PC=%d" % self.pc)
        return self.stack[-1]
    
    def execute(self, bytecode, debug=False, max_instr=1000000):
        self.pc = 0
        instr_count = 0
        
        while self.pc < len(bytecode):
            instr = bytecode[self.pc]
            opcode = (instr >> 16) & 0xFF
            operand = instr & 0xFFFF
            operand_byte = instr & 0xFF
            
            if debug and instr_count < 100:
                print(f"PC={self.pc:5d}: op={opcode:2d} operand=0x{operand:04x} stack_top={self.stack[-3:] if len(self.stack) >= 3 else self.stack}")
            
            if opcode == 0:  # PUSH immediate
                self.push(operand)
            elif opcode == 1:  # PUSH from register/input
                reg_idx = operand_byte
                if reg_idx < 3:
                    self.push(self.regs[reg_idx])
                else:
                    raise Exception(f"Invalid register index: {reg_idx}")
            elif opcode == 2:  # POP to register
                reg_idx = operand_byte
                if reg_idx < 3:
                    self.regs[reg_idx] = self.pop()
                else:
                    raise Exception(f"Invalid register index: {reg_idx}")
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
            else:
                if debug:
                    print(f"Unknown opcode: {opcode} at PC={self.pc}")
                
            self.pc += 1
            instr_count += 1
            
            if instr_count > max_instr:
                raise Exception("Max instructions exceeded")
        
        # Return top 26 elements from stack as the result
        if len(self.stack) >= 26:
            return self.stack[-26:]
        return self.stack

# Load binary and extract bytecode
with open('tiny_vm', 'rb') as f:
    data = f.read()

# Bytecode location
file_offset = 0x690c0
ptr_file_offset = 0x652a8 + 8
len_bytes = data[ptr_file_offset:ptr_file_offset+8]
bytecode_len = struct.unpack('<Q', len_bytes)[0]

bytecode_bytes = data[file_offset:file_offset+bytecode_len*4]
bytecode = [struct.unpack('<I', bytecode_bytes[i*4:i*4+4])[0] for i in range(bytecode_len)]

print(f"Loaded {len(bytecode)} instructions")

# Expected output
expected = bytes([129, 162, 253, 190, 189, 69, 44, 25, 242, 51, 201, 199, 165, 240, 188, 73, 222, 136, 182, 219, 17, 206, 31, 35, 252, 185])

# Test with a known input
test_input = "i" * 26
test_key = [0xaa] * 26

print(f"\nTesting with input: {test_input}")
vm = TinyVM(test_input, test_key)

try:
    result = vm.execute(bytecode, debug=False)
    print(f"VM result length: {len(result)}")
    if len(result) >= 26:
        output_bytes = bytes([r & 0xFF for r in result[-26:]])
        print(f"Output: {output_bytes.hex()}")
        print(f"Expected: {expected.hex()}")
        if output_bytes == expected:
            print("MATCH! Flag is:", test_input)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
