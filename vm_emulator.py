#!/usr/bin/env python3
import struct

class TinyVM:
    def __init__(self):
        self.stack = []
        self.registers = [0] * 3  # R0, R1, R2
        self.pc = 0
        
    def push(self, value):
        self.stack.append(value & 0xFFFF)
        
    def pop(self):
        if not self.stack:
            raise Exception("Stack underflow")
        return self.stack.pop()
    
    def peek(self):
        if not self.stack:
            raise Exception("Stack underflow")
        return self.stack[-1]
    
    def execute(self, bytecode, debug=False):
        self.pc = 0
        while self.pc < len(bytecode):
            instr = bytecode[self.pc]
            opcode = (instr >> 16) & 0xFF
            operand = instr & 0xFFFF
            operand_byte = instr & 0xFF
            
            if debug:
                print(f"PC={self.pc:4d}: opcode={opcode:2d}, operand=0x{operand:04x}, stack={self.stack[-5:]}")
            
            if opcode == 0:  # PUSH immediate
                self.push(operand)
            elif opcode == 1:  # PUSH from register
                reg_idx = operand_byte
                if reg_idx < len(self.registers):
                    self.push(self.registers[reg_idx])
            elif opcode == 2:  # POP to register
                reg_idx = operand_byte
                if reg_idx < len(self.registers):
                    self.registers[reg_idx] = self.pop()
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
            elif opcode == 6:  # DUP (duplicate top of stack)
                self.push(self.peek())
            elif opcode == 7:  # SWAP (swap top two elements)
                b = self.pop()
                a = self.pop()
                self.push(b)
                self.push(a)
            elif opcode == 8:  # ROT (rotate top 3 elements)
                c = self.pop()
                b = self.pop()
                a = self.pop()
                self.push(b)
                self.push(c)
                self.push(a)
            elif opcode == 9:  # OVER (copy second element to top)
                b = self.pop()
                a = self.peek()
                self.push(b)
                self.push(a)
            elif opcode == 10:  # DROP (discard top element)
                self.pop()
            elif opcode == 11:  # MUL
                b = self.pop()
                a = self.pop()
                self.push((a * b) & 0xFFFF)
            elif opcode == 12:  # EQ (check equality)
                b = self.pop()
                a = self.pop()
                self.push(1 if a == b else 0)
            else:
                if debug:
                    print(f"Unknown opcode: {opcode}")
                
            self.pc += 1
            
            # Safety check
            if self.pc > 100000:
                raise Exception("Too many instructions, possible infinite loop")

# Load the binary
with open('tiny_vm', 'rb') as f:
    data = f.read()

# Extract bytecode
virtual_addr = 0x11a20c0
base_virtual = 0x118e000
base_file = 0x55000
file_offset = base_file + (virtual_addr - base_virtual)

# Read bytecode length from pointer at 0x119e2a8
ptr_file_offset = 0x652a8 + 8  # +8 for length field
len_bytes = data[ptr_file_offset:ptr_file_offset+8]
bytecode_len = struct.unpack('<Q', len_bytes)[0]

print(f"Bytecode length: {bytecode_len} instructions")

# Read bytecode
bytecode_file_offset = file_offset
bytecode_bytes = data[bytecode_file_offset:bytecode_file_offset+bytecode_len*4]
bytecode = []
for i in range(bytecode_len):
    instr = struct.unpack('<I', bytecode_bytes[i*4:i*4+4])[0]
    bytecode.append(instr)

# Filter out padding instructions (0xaaaa patterns that don't make sense)
# Keep only valid-looking instructions
filtered_bytecode = []
for instr in bytecode:
    opcode = (instr >> 16) & 0xFF
    # Skip if it looks like padding
    if opcode == 0xaa or (instr == 0 and len(filtered_bytecode) > 0 and filtered_bytecode[-1] == 0):
        continue
    filtered_bytecode.append(instr)

print(f"Filtered bytecode length: {len(filtered_bytecode)} instructions")

# Try to run the VM with a test input
# The VM should process the input flag
test_flag = "ictf{" + "A" * 21 + "}"  # 26 chars

vm = TinyVM()
# Load test flag into registers 0-25 (as character codes)
# But first, let me understand how the VM uses inputs

print("\nAnalyzing bytecode pattern...")
print("First 100 instructions:")
for i in range(min(100, len(filtered_bytecode))):
    instr = filtered_bytecode[i]
    opcode = (instr >> 16) & 0xFF
    operand = instr & 0xFFFF
    print(f"  {i:3d}: op={opcode:2d}, operand={operand:5d} (0x{operand:04x})")
