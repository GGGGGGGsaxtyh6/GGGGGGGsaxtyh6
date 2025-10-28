#!/usr/bin/env python3

import struct
import ctypes

# Read config.bin
with open('/workspace/config.bin', 'rb') as f:
    data = f.read()

# First 4 bytes are the length
length = struct.unpack('<I', data[0:4])[0]
encrypted_flag = bytearray(data[4:4+length])
xor_key = bytearray(data[4+length:])

print(f"Length: {length}")
print(f"Encrypted flag: {encrypted_flag.decode('ascii')}")
print(f"XOR key length: {len(xor_key)}")

# Step 1: XOR with the key (fcn.0040127b at 0x402cb0)
# This is what the function does:
# for i in range(min(len(encrypted_flag), len(xor_key))):
#     encrypted_flag[i] ^= xor_key[i]

flag_xored = bytearray(encrypted_flag)
for i in range(min(len(flag_xored), len(xor_key))):
    flag_xored[i] ^= xor_key[i]

print(f"After XOR: {flag_xored.hex()}")

# Step 2: Apply the decryption algorithm from fcn.0040122b (0x402bc0)
# This function takes arg_8h (number of iterations) and modifies data at 0x40c3d0
# Looking at the code, it seems to apply a transformation based on indices

# Constants from the function
VAR_10 = 0x55  # 85
VAR_18 = 0x33  # 51  
VAR_20 = 0x0F  # 15
VAR_1 = ord('a')  # 97

# The function seems to be encrypting, so we need to reverse it
# But let's first try to understand what the original data represents

# Looking at the assembly more carefully, the algorithm at 0x402bc0 is:
# for i in range(count):
#     for j in range(length):
#         temp1 = ((j % 0xFF) & VAR_10) + ((j % 0xFF) >> 1) & VAR_10)
#         temp2 = (temp1 & VAR_18) + ((temp1 >> 2) & VAR_18)
#         value = data[j] - VAR_1  
#         value += (temp2 & VAR_20) + ((temp2 >> 4) & VAR_20)
#         data[j] = VAR_1 + (value % 26)

# This is an encryption function. To decrypt, we need to reverse it.
# Let's try to reverse-engineer by testing different approaches

# Maybe the simplest approach is: the data after XOR is already the flag?
print(f"\nTrying direct XOR result: {flag_xored.decode('latin-1', errors='ignore')}")

# Or maybe we need to treat it differently
# Let's check if picoCTF{ appears anywhere
for i in range(len(flag_xored)):
    # Try to see if we can find "picoCTF{" pattern
    if flag_xored[i] == ord('p') ^ ord('n'):
        print(f"Possible match at position {i}")

# Let me try another approach: reverse the encryption
# The encryption adds values, so decryption should subtract

def decrypt_algorithm(data, count):
    result = bytearray(data)
    VAR_10 = 0x55
    VAR_18 = 0x33
    VAR_20 = 0x0F
    VAR_1 = ord('a')
    
    # We need to reverse the process
    # The original algorithm is: new_val = (old_val - 'a' + offset) % 26 + 'a'
    # To reverse: old_val = (new_val - 'a' - offset) % 26 + 'a'
    
    for iteration in range(count):
        for j in range(len(result)):
            temp1 = ((j % 0xFF) & VAR_10) + (((j % 0xFF) >> 1) & VAR_10)
            temp2 = (temp1 & VAR_18) + ((temp1 >> 2) & VAR_18)
            offset = (temp2 & VAR_20) + ((temp2 >> 4) & VAR_20)
            
            # Reverse the operation
            value = result[j] - VAR_1
            value = (value - offset) % 26
            result[j] = VAR_1 + value
    
    return result

# Try decrypting with different iteration counts
print("\n=== Trying decryption ===")
for count in [1, 2, 3]:
    decrypted = decrypt_algorithm(encrypted_flag, count)
    print(f"Count {count}: {decrypted.decode('ascii', errors='ignore')}")
    if b'pico' in decrypted.lower():
        print(f"  -> Found 'pico'!")

# Also try on the XORed version
print("\n=== Trying decryption on XORed data ===")
# Convert non-printable to 'a' + value
normalized = bytearray()
for b in flag_xored:
    if 32 <= b < 127:  # printable ASCII
        if ord('a') <= b <= ord('z'):
            normalized.append(b)
        else:
            # Convert to lowercase letter range
            normalized.append(ord('a') + (b % 26))
    else:
        normalized.append(ord('a') + (b % 26))

print(f"Normalized: {normalized.decode('ascii')}")

for count in [1, 2, 3]:
    decrypted = decrypt_algorithm(normalized, count)
    print(f"Count {count}: {decrypted.decode('ascii', errors='ignore')}")
