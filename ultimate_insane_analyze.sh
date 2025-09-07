#!/bin/bash

echo "🔍 Análisis del Ultimate Insane Vault"
echo "======================================"
echo ""

# Información básica
echo "📊 Información del binario:"
file ultimate_insane_vault
echo "Tamaño: $(ls -lh ultimate_insane_vault | awk '{print $5}')"
echo ""

# Análisis de strings
echo "🔍 Strings HTB encontrados:"
strings ultimate_insane_vault | grep -E "HTB\{.*\}" | head -15
echo ""

# Análisis de funciones
echo "🔍 Funciones principales:"
objdump -t ultimate_insane_vault | grep -E "(main|vm_|flow_|metamorphic_)" | head -15
echo ""

# Análisis de protecciones
echo "🔍 Protecciones detectadas:"
strings ultimate_insane_vault | grep -E "(debug|analysis|metamorphic|vm)" | head -15
echo ""

# Análisis de llamadas al sistema
echo "🔍 Llamadas al sistema:"
objdump -d ultimate_insane_vault | grep -E "(syscall|int 0x80)" | head -10
echo ""

# Análisis de strings importantes
echo "🔍 Strings importantes:"
strings ultimate_insane_vault | grep -E "(metamorphic|vault|vm|encrypt)" | head -15
echo ""

echo "💡 Próximos pasos:"
echo "1. Usa gdb para análisis dinámico de la VM metamórfica"
echo "2. Analiza las funciones de la máquina virtual"
echo "3. Entiende el control flow obfuscation"
echo "4. Reversa el algoritmo de cifrado metamórfico"
echo "5. Encuentra la flag en la VM metamórfica"
echo ""
echo "🔧 Comandos útiles:"
echo "gdb ./ultimate_insane_vault"
echo "objdump -d ultimate_insane_vault > ultimate_insane_disassembly.txt"
echo "strings ultimate_insane_vault | grep HTB"
echo "radare2 -d ultimate_insane_vault"
