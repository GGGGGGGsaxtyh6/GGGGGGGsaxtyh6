#!/bin/bash

echo "🔍 Análisis Ultra del Challenge ULTRA-INSANE"
echo "============================================="
echo ""

# Información básica
echo "📊 Información del binario:"
file ultimate_challenge
echo "Tamaño: $(ls -lh ultimate_challenge | awk '{print $5}')"
echo ""

# Análisis de strings
echo "🔍 Strings HTB encontrados:"
strings ultimate_challenge | grep -E "HTB\{.*\}" | head -25
echo ""

# Análisis de funciones
echo "🔍 Funciones principales:"
objdump -t ultimate_challenge | grep -E "(main|validate|detect|obfuscat)" | head -20
echo ""

# Análisis de protecciones
echo "🔍 Protecciones detectadas:"
strings ultimate_challenge | grep -E "(debug|vm|sandbox|integrity|ptrace|analysis)" | head -20
echo ""

# Análisis de llamadas al sistema
echo "🔍 Llamadas al sistema:"
objdump -d ultimate_challenge | grep -E "(syscall|int 0x80)" | head -15
echo ""

# Análisis de strings importantes
echo "🔍 Strings importantes:"
strings ultimate_challenge | grep -E "(smurf|treasure|flag|validate|ultra)" | head -20
echo ""

# Análisis de constantes
echo "🔍 Constantes importantes:"
objdump -s ultimate_challenge | grep -E "(0x[0-9a-f]{8})" | head -15
echo ""

# Análisis de secciones
echo "🔍 Secciones del binario:"
readelf -S ultimate_challenge | head -25
echo ""

# Análisis de símbolos
echo "🔍 Símbolos importantes:"
nm ultimate_challenge | grep -E "(main|validate|detect)" | head -20
echo ""

echo "💡 Próximos pasos ultra:"
echo "1. Usa gdb para análisis dinámico ultra"
echo "2. Bypasea las protecciones anti-debugging ultra-avanzadas"
echo "3. Analiza las funciones de validación ultra"
echo "4. Encuentra la flag real ultra-ofuscada en el código"
echo "5. Verifica con el algoritmo de validación ultra"
echo ""
echo "🔧 Comandos útiles ultra:"
echo "gdb ./ultimate_challenge"
echo "objdump -d ultimate_challenge > ultra_disassembly.txt"
echo "strings ultimate_challenge | grep HTB"
echo "radare2 -d ultimate_challenge"
