#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'

print("=== CALCULANDO OFFSETS EXACTOS ===\n")

# Layout del stack basado en desensamblado
print("Stack layout en vuln():")
print("rbp-740: choice")
print("rbp-736: entries[0].name")
print("rbp-728: entries[0].msg")
print("...")
print("rbp-12: feedback[0]")
print("rbp-4: total_entries")
print("rbp+0: saved rbp")
print("rbp+8: return address\n")

# Calcular qué índice negativo necesito
print("Calculando índice negativo para escribir en return address:")
print("entries[i].msg está en: rbp-736 + i*72 + 8 = rbp-728 + i*72")
print("Para llegar a return address (rbp+8):")
print("rbp-728 + i*72 = rbp+8")
print("i*72 = 736")
print("i = 736/72 = 10.222...\n")

print("No puedo llegar exactamente al return address con índice negativo.")
print("PERO con msg[64] puedo escribir 64 bytes desde entries[i].msg\n")

# Intentar con diferentes índices
print("Analizando qué puedo sobrescribir con cada índice:\n")
for i in range(11, 15):
    msg_start = -728 + i*72
    msg_end = msg_start + 64
    print(f"entries[{i}].msg: rbp{msg_start:+d} a rbp{msg_end:+d}")
    if msg_start <= 8 <= msg_end:
        print(f"  *** PUEDE SOBRESCRIBIR RETURN ADDRESS! ***")
        bytes_before_ret = 8 - msg_start
        print(f"  Return address está a {bytes_before_ret} bytes desde inicio del msg")

print("\n=== ESTRATEGIA FINAL ===")
print("MEJOR OPCIÓN: Usar feedback overflow (opción 3)")
print("1. Agregar entrada con shellcode")
print("2. Usar opción 3 para overflow feedback")
print("3. Payload de 32 bytes:")
print("   [padding 8 bytes][padding 4 bytes][saved_rbp 8 bytes][ret_addr 8 bytes]")
print("   Total: 8+4+8+8 = 28 bytes (caben en 32)")
print("\nProblema: necesito dirección del stack para apuntar al shellcode")
print("Solución: probar direcciones comunes o usar ret2libc/ROP")
