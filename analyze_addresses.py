#!/usr/bin/env python3

# From GDB output:
# First buffer is at: 0x7fffffffe870
# Second buffer is at: 0x7fffffffe8b0

first_buf = 0x7fffffffe870
second_buf = 0x7fffffffe8b0

print(f"First buffer:  0x{first_buf:016x}")
print(f"Second buffer: 0x{second_buf:016x}")
print(f"Distance: {second_buf - first_buf} = 0x{second_buf - first_buf:x}")

# After pivot and pop rbp and ret:
# RIP will point to bytes [8:16] of second buffer
# RSP will point to byte 16 of second buffer

rip_after_ret = second_buf + 8
rsp_after_ret = second_buf + 16

print(f"\nAfter ret:")
print(f"RIP will be at: 0x{rip_after_ret:016x}")
print(f"RSP will be at: 0x{rsp_after_ret:016x}")

# We put JMP at bytes [8:9] (2 bytes)
# JMP instruction is at: second_buf + 8
# After JMP executes, RIP = second_buf + 10 (pointing after the JMP instruction)

rip_after_jmp_instruction = second_buf + 10

print(f"\nAfter JMP instruction read:")
print(f"RIP will be at: 0x{rip_after_jmp_instruction:016x} (pointing after the 2-byte JMP)")

# We want to jump to first_buf
target = first_buf

# JMP offset = target - rip_after_jmp
offset = target - rip_after_jmp_instruction

print(f"\nJMP offset calculation:")
print(f"Target: 0x{target:016x}")
print(f"Current RIP (after JMP): 0x{rip_after_jmp_instruction:016x}")
print(f"Offset: {offset} = 0x{offset:x}")

# For 8-bit signed offset (jmp short)
if offset < 0:
    offset_byte = (256 + offset) & 0xff
else:
    offset_byte = offset & 0xff

print(f"As 8-bit value: 0x{offset_byte:02x}")
print(f"JMP instruction: EB {offset_byte:02x}")
