#!/usr/bin/env python3
import struct

with open('/workspace/config.bin', 'rb') as f:
    file_data = f.read()

length = struct.unpack('<I', file_data[0:4])[0]
buffer_data = file_data[4:]
encrypted_data = list(buffer_data[0:length])  # Use list for easier debugging
xor_key = list(buffer_data[length+1:length+1+length])

print(f"Initial data: {''.join([chr(c) for c in encrypted_data])}")
print(f"XOR key: {bytes(xor_key).hex()}\n")

def obfuscate_with_trace(data, iterations, trace_indices=[0, 1, 2]):
    """Trace specific indices through the algorithm"""
    result = list(data)
    
    VAR_10 = 0x55  # 0101_0101
    VAR_18 = 0x33  # 0011_0011
    VAR_20 = 0x0F  # 0000_1111
    VAR_1 = ord('a')  # 97
    
    for iteration in range(iterations):
        print(f"\n--- Iteration {iteration} ---")
        for i in range(len(result)):
            # Trace specific indices
            trace = (i in trace_indices)
            
            # Calculate idx_mod = i % 0xFF
            idx_mod = i % 0xFF
            
            # temp1 = (idx_mod & VAR_10) + ((idx_mod >> 1) & VAR_10)
            part1 = idx_mod & VAR_10
            part2 = (idx_mod >> 1) & VAR_10
            temp1 = part1 + part2
            
            if trace:
                print(f"  i={i}: idx_mod=0x{idx_mod:02x}, part1=0x{part1:02x}, part2=0x{part2:02x}, temp1=0x{temp1:02x}")
            
            # temp2 = (temp1 & VAR_18) + ((temp1 >> 2) & VAR_18)
            part3 = temp1 & VAR_18
            part4 = (temp1 >> 2) & VAR_18
            temp2 = part3 + part4
            
            if trace:
                print(f"       part3=0x{part3:02x}, part4=0x{part4:02x}, temp2=0x{temp2:02x}")
            
            # Get current character
            current_char = result[i]
            
            # value = current_char - VAR_1
            value = current_char - VAR_1
            
            # offset = (temp2 & VAR_20) + ((temp2 >> 4) & VAR_20)
            part5 = temp2 & VAR_20
            part6 = (temp2 >> 4) & VAR_20
            offset = part5 + part6
            
            if trace:
                print(f"       current='{chr(current_char)}'(0x{current_char:02x}), value={value}, offset={offset}")
            
            # value = (value + offset) % 26
            value = (value + offset) % 26
            
            # new_char = VAR_1 + value
            new_char = VAR_1 + value
            
            if trace:
                print(f"       new_value={value}, new_char='{chr(new_char)}'(0x{new_char:02x})")
            
            result[i] = new_char
        
        print(f"After iteration {iteration}: {''.join([chr(c) for c in result[:20]])}...")
    
    return result

# Test with 1 iteration
print("=== Testing with 1 iteration ===")
obf_data = obfuscate_with_trace(encrypted_data, 1, trace_indices=[0, 1, 2, 3, 4])

# XOR
result = list(xor_key)
for i in range(min(len(result), len(obf_data))):
    result[i] ^= obf_data[i]

result_bytes = bytes(result)
print(f"\nResult: {result_bytes}")
try:
    print(f"UTF-8: {result_bytes.decode('utf-8')}")
except:
    print(f"UTF-8: {result_bytes.decode('utf-8', errors='ignore')}")
