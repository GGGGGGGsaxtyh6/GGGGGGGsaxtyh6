#!/usr/bin/env python3
from pwn import *

# Analizar el layout exacto del stack
print("=== ANÁLISIS DE VULNERABILIDADES ===\n")

print("1. ESTRUCTURA DE DATOS:")
print("   typedef struct entry {")
print("       char name[8];")
print("       char msg[64];")
print("   } entry_t;  // Total: 72 bytes\n")

print("2. VARIABLES LOCALES EN vuln():")
print("   char feedback[8];")
print("   entry_t entries[10];  // 720 bytes")
print("   int total_entries = 0;")
print("   int choice = -1;\n")

print("3. STACK LAYOUT (basado en desensamblado):")
print("   sub $0x2f0,%rsp  => 752 bytes de stack frame")
print("   rbp-740 (-0x2e4): choice (4 bytes)")
print("   rbp-736 (-0x2e0): entries[0] (inicio del array)")
print("   rbp-664: entries[1]")
print("   rbp-592: entries[2]")
print("   ...") 
print("   rbp-16: entries[9] (último elemento)")
print("   rbp-12 (-0xc): feedback[0-7] (8 bytes)")
print("   rbp-4: total_entries (4 bytes)")
print("   rbp+0: saved rbp (8 bytes)")
print("   rbp+8: return address (8 bytes)\n")

print("4. VULNERABILIDAD PRINCIPAL:")
print("   Opción 3 (exit/feedback):")
print("   - fgets(feedback, NAME_LEN, stdin) donde NAME_LEN=32")
print("   - feedback solo tiene 8 bytes!")
print("   - Overflow: 32 bytes desde rbp-12")
print("   - Puede sobrescribir: total_entries(4) + saved_rbp(8) + ret_addr(8)")
print("   - Total controlable: 20 bytes después de feedback[7]\n")

print("5. VULNERABILIDAD SECUNDARIA:")
print("   Opción 2 (send message):")
print("   - NO verifica choice < 0, solo choice >= total_entries")
print("   - Con choice negativo puedo escribir ANTES del array")
print("   - entries[choice].msg = rbp-736 + choice*72 + 8\n")

print("6. CÁLCULO PARA ÍNDICE NEGATIVO:")
for i in range(-15, -5):
    addr_offset = -736 + i*72 + 8
    print(f"   entries[{i:3d}].msg = rbp{addr_offset:+5d}")
    if addr_offset >= 0 and addr_offset <= 8:
        print(f"      ^^^ ESTO APUNTA AL RETURN ADDRESS!")

print("\n7. ESTRATEGIA DE EXPLOTACIÓN:")
print("   OPCIÓN A - Overflow directo con feedback:")
print("   1. Agregar entry con shellcode en entries[0].name o .msg")
print("   2. Opción 3: overflow feedback con 32 bytes")
print("   3. Bytes 0-7: basura (feedback)")
print("   4. Bytes 8-11: total_entries (o basura)")
print("   5. Bytes 12-19: saved rbp (o basura)")
print("   6. Bytes 20-27: nueva dirección de retorno (shellcode addr)")
print("   7. Return a shellcode y obtener shell\n")

print("   OPCIÓN B - Índice negativo:")
print("   1. Calcular índice negativo que apunte cerca del return address")
print("   2. Usar overflow del msg[64] para alcanzar return address")
print("   3. Problema: necesito índice exacto\n")

print("8. PROTECCIONES:")
print("   - NO PIE: direcciones fijas (0x400000)")
print("   - NO Canary: puedo sobrescribir ret sin detección")
print("   - Stack ejecutable: shellcode funciona")
print("   - RWX segments: máxima flexibilidad\n")

print("9. DESAFÍO:")
print("   - Necesito saber dirección exacta del stack para shellcode")
print("   - O usar ROP gadgets (pero con stack ejecutable no es necesario)")
print("   - Probar direcciones comunes del stack o buscar leak\n")

print("=== ANÁLISIS COMPLETO ===")
