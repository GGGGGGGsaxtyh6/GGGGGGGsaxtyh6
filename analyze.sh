#!/bin/bash

echo "🔍 Análisis del challenge INSANE"
echo "================================"
echo ""

echo "📊 Información del binario:"
file smurf_treasure
echo "Tamaño: $(ls -lh smurf_treasure | awk '{print $5}')"
echo ""

echo "🔍 Strings HTB encontrados:"
strings smurf_treasure | grep -E "HTB\{.*\}" | head -20
echo ""

echo "🔍 Funciones principales:"
objdump -t smurf_treasure | grep -E "(main|validate|detect)" | head -10
echo ""

echo "🔍 Protecciones detectadas:"
strings smurf_treasure | grep -E "(debug|vm|sandbox|integrity)" | head -10
echo ""

echo "💡 Próximos pasos:"
echo "1. Analiza el assembly con: objdump -d smurf_treasure"
echo "2. Busca la función main y las funciones de validación"
echo "3. Identifica las protecciones anti-debugging"
echo "4. Bypasea las protecciones con gdb"
echo "5. Encuentra la flag real en el código"
