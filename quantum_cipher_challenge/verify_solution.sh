#!/bin/bash

echo "=== Verificación de Solución ==="
echo ""

if [ ! -f "quantum_cipher" ]; then
    echo "ERROR: Binario no encontrado"
    exit 1
fi

echo "✓ Binario encontrado"

# Verificar que el binario es ejecutable
if [ ! -x "quantum_cipher" ]; then
    echo "ERROR: Binario no es ejecutable"
    exit 1
fi

echo "✓ Binario es ejecutable"

# Verificar tamaño del binario
size=$(stat -c%s quantum_cipher)
echo "✓ Tamaño del binario: $size bytes"

# Verificar que no hay símbolos de debug
if nm quantum_cipher 2>/dev/null | wc -l | grep -q "^0$"; then
    echo "✓ Símbolos de debug eliminados"
else
    echo "✗ Símbolos de debug presentes"
fi

echo ""
echo "El reto está listo para ser resuelto."
echo "Ejecuta './quantum_cipher' para comenzar."
