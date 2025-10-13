#!/usr/bin/env python3
"""
Análisis exhaustivo del índice negativo

Con choice negativo, puedo escribir ANTES del array entries.
¿Hay algo útil antes del array que pueda sobrescribir?

entries está en rbp-736
¿Qué hay en rbp-740 a rbp-737? ¡La variable choice!

Si sobrescribo choice con un valor específico, ¿puedo causar comportamiento útil?

No directamente, pero déjame verificar qué más hay antes del array.
"""

print("=== LAYOUT DEL STACK EN vuln() ===")
print("rbp+8: return address")
print("rbp+0: saved rbp")
print("rbp-4: total_entries")
print("rbp-12: feedback[0-7]")
print("rbp-16 a rbp-735: [espacio no usado o variables]")
print("rbp-736: entries[0].name[0-7]")
print("rbp-728: entries[0].msg[0-63]")
print("rbp-740: choice")
print()

print("=== ANÁLISIS DE ÍNDICES NEGATIVOS ===")
print("entries[i].name está en rbp + (-736 + i*72)")
print("entries[i].msg está en rbp + (-728 + i*72)")
print()

# Analizar qué puedo sobrescribir con índice negativo

print("Con opción 1 (agregar nombre):")
print("  fgets(entries[total_entries].name, NAME_LEN, stdin)")
print("  Lee 32 bytes pero name solo tiene 8 bytes")
print("  Overflow de 24 bytes!")
print()

print("Probando overflow de name:")
# entries[0].name está en rbp-736
# Si leo 32 bytes, escribo hasta rbp-736+32 = rbp-704
print("entries[0].name en rbp-736")
print("Leyendo 32 bytes: rbp-736 a rbp-705")
print("entries[0].msg empieza en rbp-728")
print("¡Puedo sobrescribir parte de entries[0].msg con overflow de name!")
print()

print("Estrategia:")
print("1. Agregar entrada 0 con nombre que contenga ROP chain (32 bytes)")
print("2. Este ROP se escribe en name (8) + parte de msg (24)")
print("3. Agregar más entradas hasta 10")
print("4. Usar feedback overflow para saltar a entries[0].name")
print("5. El ROP chain se ejecuta")
print()

print("Problema: ¿Cuál es la dirección de entries[0].name?")
print("entries[0].name = rbp - 736")
print("Necesito conocer rbp, que tiene ASLR...")
