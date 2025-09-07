#!/bin/bash

# Script de análisis avanzado para el challenge INSANE
# Proporciona análisis detallado del binario

echo "🔍 Análisis Avanzado del Challenge INSANE"
echo "=========================================="
echo ""

# Información básica
echo "📊 Información del binario:"
file smurf_treasure
echo "Tamaño: $(ls -lh smurf_treasure | awk '{print $5}')"
echo ""

# Análisis de strings
echo "🔍 Strings HTB encontrados:"
strings smurf_treasure | grep -E "HTB\{.*\}" | head -20
echo ""

# Análisis de funciones
echo "🔍 Funciones principales:"
objdump -t smurf_treasure | grep -E "(main|validate|detect|obfuscat)" | head -15
echo ""

# Análisis de protecciones
echo "🔍 Protecciones detectadas:"
strings smurf_treasure | grep -E "(debug|vm|sandbox|integrity|ptrace)" | head -15
echo ""

# Análisis de llamadas al sistema
echo "🔍 Llamadas al sistema:"
objdump -d smurf_treasure | grep -E "(syscall|int 0x80)" | head -10
echo ""

# Análisis de strings importantes
echo "🔍 Strings importantes:"
strings smurf_treasure | grep -E "(smurf|treasure|flag|validate)" | head -15
echo ""

# Análisis de constantes
echo "🔍 Constantes importantes:"
objdump -s smurf_treasure | grep -E "(0x[0-9a-f]{8})" | head -10
echo ""

# Análisis de secciones
echo "🔍 Secciones del binario:"
readelf -S smurf_treasure | head -20
echo ""

# Análisis de símbolos
echo "🔍 Símbolos importantes:"
nm smurf_treasure | grep -E "(main|validate|detect)" | head -15
echo ""

echo "💡 Próximos pasos:"
echo "1. Usa gdb para análisis dinámico"
echo "2. Bypasea las protecciones anti-debugging"
echo "3. Analiza las funciones de validación"
echo "4. Encuentra la flag real en el código"
echo "5. Verifica con el algoritmo de validación"
echo ""
echo "🔧 Comandos útiles:"
echo "gdb ./smurf_treasure"
echo "objdump -d smurf_treasure > disassembly.txt"
echo "strings smurf_treasure | grep HTB"
echo "radare2 -d smurf_treasure"
