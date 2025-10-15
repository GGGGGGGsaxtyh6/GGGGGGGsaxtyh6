#!/usr/bin/env python3
import struct

with open('/workspace/config.bin', 'rb') as f:
    file_data = f.read()

length = struct.unpack('<I', file_data[0:4])[0]
buffer_data = file_data[4:]
encrypted_data = bytearray(buffer_data[0:length])
xor_key = bytearray(buffer_data[length+1:length+1+length])

print(f"Length: {length}")
print(f"Encrypted: {encrypted_data.decode('ascii')}")
print(f"Key: {xor_key.hex()}\n")

def obfuscate_exact(data, iterations):
    """Exact implementation matching assembly at 0x402bc0"""
    result = bytearray(data)
    
    # var_10h = 0x55, var_18h = 0x33, var_20h = 0x0F, var_1h = 0x61
    VAR_10 = 0x55
    VAR_18 = 0x33
    VAR_20 = 0x0F
    VAR_1 = 0x61
    
    data_len = length  # from [0x40c3d8]
    
    # Outer loop: for(var_ch = 0; var_ch < iterations; var_ch++)
    for iteration in range(iterations):
        # Inner loop: for(var_8h = 0; var_8h < data_len; var_8h++)
        for i in range(data_len):
            # 0x402c15-0x402c37: Calculate temp values
            # eax = var_8h; edx = eax % 0xFF
            idx_mod = i % 0xFF
            
            # ecx = edx & VAR_10
            ecx = idx_mod & VAR_10
            
            # edx = (idx_mod % 0xFF) >> 1; edx = edx & VAR_10
            edx = (idx_mod >> 1) & VAR_10
            
            # ecx = ecx + edx
            ecx = ecx + edx
            
            # var_14h = ecx (temp1)
            temp1 = ecx
            
            # 0x402c3a-0x402c4b: Calculate temp2
            # edx = VAR_18 & temp1
            edx = VAR_18 & temp1
            
            # eax = temp1 >> 2; eax = eax & VAR_18
            eax = (temp1 >> 2) & VAR_18
            
            # edx = edx + eax
            edx = edx + eax
            
            # var_1ch = edx (temp2)
            temp2 = edx
            
            # 0x402c4e-0x402c7f: Transform byte
            # ecx = sign_extend(VAR_1)
            ecx = VAR_1
            
            # edx = [0x40c3d0 + var_8h]
            # eax = zero_extend(byte at edx)
            eax = result[i]
            
            # edx = sign_extend(VAR_1)
            edx = VAR_1
            
            # eax = eax - edx
            eax = eax - edx
            
            # edx = VAR_20 & temp2
            edx = VAR_20 & temp2
            
            # eax = eax + edx
            eax = eax + edx
            
            # edx = temp2 >> 4; edx = edx & VAR_20
            edx = (temp2 >> 4) & VAR_20
            
            # eax = eax + edx
            eax = eax + edx
            
            # edx:eax = signed_div(eax, 0x1A)
            # edx = remainder
            edx = (eax % 26 + 26) % 26 if eax < 0 else eax % 26
            
            # ecx = ecx + edx
            ecx = ecx + edx
            
            # [0x40c3d0 + var_8h] = cl
            result[i] = ecx & 0xFF
    
    return result

def xor_buffers(key, data):
    """Exact implementation matching assembly at 0x402cb0"""
    result = bytearray(key)
    
    # for(var_4h = 0; var_4h < length; var_4h++)
    for i in range(min(len(result), len(data))):
        # edx = [0x40c3d4 + var_4h]
        # eax = zero_extend(byte at edx)
        byte_key = result[i]
        
        # ecx = arg_8h + var_4h
        # edx = zero_extend(byte at ecx)
        byte_data = data[i]
        
        # eax = eax XOR edx
        eax = byte_key ^ byte_data
        
        # [0x40c3d4 + var_4h] = al
        result[i] = eax & 0xFF
    
    return result

print("=== Testing with exact assembly simulation ===\n")

for iterations in range(0, 5):
    obf_data = obfuscate_exact(encrypted_data, iterations)
    result = xor_buffers(xor_key, obf_data)
    
    print(f"Iterations: {iterations}")
    print(f"  Obfuscated: {obf_data.decode('ascii')}")
    print(f"  Result hex: {result.hex()}")
    
    try:
        text = result.decode('utf-8')
        print(f"  UTF-8: {text}")
        if 'picoCTF' in text:
            print("  ^^^ FOUND THE FLAG!")
    except:
        text = result.decode('utf-8', errors='ignore')
        print(f"  UTF-8 (ignore): {text}")
    
    if '{' in text and '}' in text:
        print(f"  ^^^ Contains braces!")
    
    print()
