#!/usr/bin/env python3

print("=== CÁLCULO CON ÍNDICES NEGATIVOS ===\n")

print("entries[i].msg está en: rbp + (-736 + i*72 + 8)")
print("                      = rbp + (-728 + i*72)\n")

print("Verificando índices negativos:\n")
for i in range(-20, 15):
    msg_start = -728 + i*72
    msg_end = msg_start + 63  # msg tiene 64 bytes (0-63)
    
    # Verificar si puede sobrescribir cosas importantes
    can_write_feedback = (msg_start <= -12 <= msg_end)
    can_write_total = (msg_start <= -4 <= msg_end)
    can_write_rbp = (msg_start <= 0 <= msg_end)
    can_write_ret = (msg_start <= 8 <= msg_end)
    
    if can_write_feedback or can_write_total or can_write_rbp or can_write_ret:
        print(f"entries[{i:3d}].msg: rbp{msg_start:+5d} to rbp{msg_end:+5d}")
        
        if can_write_feedback:
            offset_to_feedback = -12 - msg_start
            print(f"            *** Puede sobrescribir FEEDBACK (offset {offset_to_feedback})***")
        if can_write_total:
            offset_to_total = -4 - msg_start
            print(f"            *** Puede sobrescribir TOTAL_ENTRIES (offset {offset_to_total})***")
        if can_write_rbp:
            offset_to_rbp = 0 - msg_start
            print(f"            *** Puede sobrescribir SAVED_RBP (offset {offset_to_rbp})***")
        if can_write_ret:
            offset_to_ret = 8 - msg_start
            print(f"            *** Puede sobrescribir RETURN ADDRESS (offset {offset_to_ret})***")
        print()

print("\n=== ESTRATEGIAS POSIBLES ===\n")
print("ESTRATEGIA 1: Índice negativo con overflow")
print("  - Usar índice que me acerque al return address")
print("  - Overflow de msg[64] para llegar al return address\n")

print("ESTRATEGIA 2: Feedback overflow (MÁS SIMPLE)")
print("  - Opción 3 lee 32 bytes en feedback[8]")
print("  - Payload: 8 bytes + 4 bytes + 8 bytes + 8 bytes = 28 bytes")
print("  - Sobrescribe directamente el return address\n")

print("ESTRATEGIA 2 es más confiable y directa!")
