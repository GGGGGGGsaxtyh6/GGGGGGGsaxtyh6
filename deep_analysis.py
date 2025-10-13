#!/usr/bin/env python3
"""
Análisis profundo de todas las opciones

Veamos las vulnerabilidades disponibles:
1. feedback overflow: 32 bytes en 8 bytes buffer
2. name overflow: 32 bytes en 8 bytes buffer  
3. Índice negativo no verificado en opción 2

Opciones de explotación:

OPCIÓN A: Feedback overflow + vuln loop
- Establecer total_entries a valor alto con feedback overflow
- Returnar a mitad de vuln() (después de while loop)
- Pero esto no funciona porque las variables se reinicializan

OPCIÓN B: Name overflow + feedback overflow
- Colocar ROP chain con name overflow (24 bytes overflow a .msg)
- Usar feedback para saltar a él
- Problema: necesito dirección del stack

OPCIÓN C: Índice negativo extremo
- ¿Puedo escribir en el stack frame de main()?
- main está ENCIMA de vuln en el stack
- main's stack frame está en rbp_vuln + algo

Déjame calcular...
