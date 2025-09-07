#!/bin/bash

echo "🔍 Análisis del Quantum Vault"
echo "=============================="
echo ""

# Información básica
echo "📊 Información del binario:"
file quantum_vault
echo "Tamaño: $(ls -lh quantum_vault | awk '{print $5}')"
echo ""

# Análisis de strings
echo "🔍 Strings HTB encontrados:"
strings quantum_vault | grep -E "HTB\{.*\}" | head -15
echo ""

# Análisis de funciones
echo "🔍 Funciones principales:"
objdump -t quantum_vault | grep -E "(main|vm_|flow_|quantum_)" | head -15
echo ""

# Análisis de protecciones
echo "🔍 Protecciones detectadas:"
strings quantum_vault | grep -E "(debug|analysis|quantum|vm)" | head -15
echo ""

# Análisis de llamadas al sistema
echo "🔍 Llamadas al sistema:"
objdump -d quantum_vault | grep -E "(syscall|int 0x80)" | head -10
echo ""

# Análisis de strings importantes
echo "🔍 Strings importantes:"
strings quantum_vault | grep -E "(quantum|vault|vm|encrypt)" | head -15
echo ""

echo "💡 Próximos pasos:"
echo "1. Usa gdb para análisis dinámico de la VM"
echo "2. Analiza las funciones de la máquina virtual"
echo "3. Entiende el control flow flattening"
echo "4. Reversa el algoritmo de cifrado cuántico"
echo "5. Encuentra la flag en la VM"
echo ""
echo "🔧 Comandos útiles:"
echo "gdb ./quantum_vault"
echo "objdump -d quantum_vault > quantum_disassembly.txt"
echo "strings quantum_vault | grep HTB"
echo "radare2 -d quantum_vault"
