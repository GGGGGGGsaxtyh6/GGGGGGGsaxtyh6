# Análisis del reto "handoff"

## Vulnerabilidades identificadas:
1. **Buffer overflow en feedback**: lee 32 bytes en buffer de 8 bytes (línea 66)
2. **Buffer overflow en name**: lee 32 bytes en campo de 8 bytes (línea 44) 
3. **Índice negativo sin verificar**: permite escribir fuera de bounds (línea 55)

## Protecciones del binario:
- ❌ No PIE (direcciones fijas)
- ❌ No Canary 
- ✅ Stack ejecutable (RWX)
- Gadgets ROP disponibles: pop_rdi @ 0x4014b3

## Limitación principal:
Con feedback overflow de 32 bytes solo puedo controlar:
- 8 bytes: feedback
- 4 bytes: total_entries
- 8 bytes: saved_rbp
- 8 bytes: return_address
- 4 bytes: extra

Esto NO es suficiente para ROP chain completo (leak + system).

## Estrategias intentadas sin éxito:
1. Shellcode directo con bruteforce de direcciones del stack
2. ret2libc con guess de direcciones de libc
3. Stack pivoting (necesito zona controlada con dirección fija)
4. Índice negativo para sobrescribir return de main (fuera de rango)
5. Combinaciones de vulnerabilidades

## Posible solución que requiere más investigación:
El reto se llama "handoff" sugiriendo "pasar" algo entre funciones.
Quizás la técnica correcta involucra:
- Usar el name overflow (24 bytes a .msg) para colocar ROP chain largo
- Combinar con feedback overflow de manera específica
- O hay alguna dirección del stack predecible en el entorno del CTF

Sin acceso a writeups y con las restricciones actuales, no puedo completar el exploit.
