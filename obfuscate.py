#!/usr/bin/env python3
"""
Script de ofuscación adicional para el challenge
Añade más capas de protección y confusión
"""

import os
import random
import string

def add_fake_functions():
    """Añade funciones falsas al binario para confundir"""
    fake_functions = [
        "void fake_validation() { printf(\"Fake validation passed\"); }",
        "int fake_check(char* input) { return strcmp(input, \"fake\"); }",
        "void fake_decrypt() { printf(\"Fake decryption\"); }",
        "int fake_hash(char* data) { return strlen(data) * 42; }",
        "void fake_anti_debug() { printf(\"Fake anti-debug\"); }"
    ]
    
    with open('fake_functions.c', 'w') as f:
        f.write("#include <stdio.h>\n#include <string.h>\n\n")
        for func in fake_functions:
            f.write(func + "\n\n")

def create_decoy_files():
    """Crea archivos de engaño"""
    decoy_content = """
# Decoy File - No es la flag real
# Este archivo es solo para confundir

FLAG_FAKE_1=HTB{this_is_definitely_fake}
FLAG_FAKE_2=HTB{not_the_real_flag_at_all}
FLAG_FAKE_3=HTB{decoy_flag_here}

# La flag real está en otro lugar
# Pista: Busca en el binario compilado
"""
    
    with open('flags.txt', 'w') as f:
        f.write(decoy_content)
    
    # Crear un script de "solución" falso
    fake_solution = """#!/bin/bash
# Script de solución falso
echo "Analizando el binario..."
echo "Encontrada flag: HTB{fake_solution_script}"
echo "Esta no es la flag real!"
"""
    
    with open('solve.sh', 'w') as f:
        f.write(fake_solution)
    
    os.chmod('solve.sh', 0o755)

def add_hex_obfuscation():
    """Añade ofuscación hexadecimal"""
    hex_data = """
# Datos hexadecimales ofuscados
# Estos datos contienen información sobre la flag real
# Pero están ofuscados para dificultar el análisis

OBFUSCATED_DATA_1=0x4854427b736d7572665f7734735f683372335f616e645f73305f7734735f793075725f666c34677d
OBFUSCATED_DATA_2=0x536d75726620776173206865726520616e6420736f2077617320796f757220666c6167
OBFUSCATED_DATA_3=0x4854427b736d7572665f7734735f683372335f616e645f73305f7734735f793075725f666c34677d

# Para decodificar, convierte de hex a ASCII
# Pista: La flag real está en estos datos
"""
    
    with open('obfuscated_data.txt', 'w') as f:
        f.write(hex_data)

def create_hint_files():
    """Crea archivos con pistas reales"""
    hint1 = """
# Pista 1: Análisis Estático
# Usa el comando 'strings' para encontrar strings en el binario
# La flag real comienza con: HTB{smurf_

# Comandos útiles:
# strings challenge | grep HTB
# objdump -d challenge
# hexdump -C challenge
"""
    
    hint2 = """
# Pista 2: Análisis Dinámico
# El binario tiene protecciones anti-debugging
# Puedes bypasearlas modificando el código o usando gdb

# Comandos útiles:
# gdb ./challenge
# (gdb) set environment LD_PRELOAD=/lib/x86_64-linux-gnu/libc.so.6
# (gdb) run HTB{test}
"""
    
    hint3 = """
# Pista 3: La Flag Real
# La flag correcta es: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}
# Pero debes encontrarla por ti mismo usando reverse engineering

# El algoritmo de validación está en la función main()
# Verifica que la entrada tenga exactamente 32 caracteres
# Y que coincida con el patrón esperado
"""
    
    with open('hint1.txt', 'w') as f:
        f.write(hint1)
    
    with open('hint2.txt', 'w') as f:
        f.write(hint2)
    
    with open('hint3.txt', 'w') as f:
        f.write(hint3)

def main():
    print("🔧 Añadiendo ofuscación adicional...")
    
    add_fake_functions()
    create_decoy_files()
    add_hex_obfuscation()
    create_hint_files()
    
    print("✅ Ofuscación completada")
    print("📁 Archivos creados:")
    print("  - fake_functions.c (funciones falsas)")
    print("  - flags.txt (flags falsas)")
    print("  - solve.sh (script de solución falso)")
    print("  - obfuscated_data.txt (datos ofuscados)")
    print("  - hint1.txt, hint2.txt, hint3.txt (pistas)")
    
    print("\n🎯 El challenge está listo!")
    print("💡 Para resolverlo, los participantes deben:")
    print("  1. Analizar el binario con herramientas de reversing")
    print("  2. Bypasear las protecciones anti-debugging")
    print("  3. Identificar las flags falsas vs la real")
    print("  4. Encontrar el algoritmo de validación")
    print("  5. Determinar la flag correcta")

if __name__ == "__main__":
    main()