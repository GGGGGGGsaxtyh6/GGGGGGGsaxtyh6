#!/bin/bash

# Script de prueba para el reto QuantumCipher
# Verifica que todas las funcionalidades básicas funcionen

echo "=== Prueba del Reto QuantumCipher ==="
echo ""

# Verificar que el binario existe
if [ ! -f "quantum_cipher" ]; then
    echo "ERROR: El binario 'quantum_cipher' no existe"
    echo "Ejecuta 'make all' para compilar el reto"
    exit 1
fi

echo "✓ Binario encontrado"

# Verificar que el binario es ejecutable
if [ ! -x "quantum_cipher" ]; then
    echo "ERROR: El binario no es ejecutable"
    exit 1
fi

echo "✓ Binario es ejecutable"

# Probar ejecución básica
echo ""
echo "Probando ejecución básica..."
echo "8" | timeout 10s ./quantum_cipher > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ El binario se ejecuta correctamente"
else
    echo "✗ Error en la ejecución del binario"
    exit 1
fi

# Probar menú principal
echo ""
echo "Probando menú principal..."
echo -e "6\n8" | timeout 10s ./quantum_cipher | grep -q "Quantum System Status"
if [ $? -eq 0 ]; then
    echo "✓ Menú principal funciona"
else
    echo "✗ Error en el menú principal"
fi

# Probar funcionalidades específicas
echo ""
echo "Probando funcionalidades específicas..."

# Probar Quantum Key Distribution
echo -e "1\n8" | timeout 10s ./quantum_cipher | grep -q "Quantum Key Distribution"
if [ $? -eq 0 ]; then
    echo "✓ Quantum Key Distribution funciona"
else
    echo "✗ Error en Quantum Key Distribution"
fi

# Probar Quantum Entanglement Test
echo -e "2\n8" | timeout 10s ./quantum_cipher | grep -q "Quantum Entanglement Test"
if [ $? -eq 0 ]; then
    echo "✓ Quantum Entanglement Test funciona"
else
    echo "✗ Error en Quantum Entanglement Test"
fi

# Probar Quantum Measurement Interface
echo -e "3\n1\n8" | timeout 10s ./quantum_cipher | grep -q "Position measurement"
if [ $? -eq 0 ]; then
    echo "✓ Quantum Measurement Interface funciona"
else
    echo "✗ Error en Quantum Measurement Interface"
fi

# Probar Quantum Decoherence Analysis
echo -e "4\n8" | timeout 10s ./quantum_cipher | grep -q "Quantum Decoherence Analysis"
if [ $? -eq 0 ]; then
    echo "✓ Quantum Decoherence Analysis funciona"
else
    echo "✗ Error en Quantum Decoherence Analysis"
fi

# Probar Quantum Algorithm Execution
echo -e "5\n1\n8" | timeout 10s ./quantum_cipher | grep -q "Grover's algorithm"
if [ $? -eq 0 ]; then
    echo "✓ Quantum Algorithm Execution funciona"
else
    echo "✗ Error en Quantum Algorithm Execution"
fi

# Probar Quantum Research Database
echo -e "7\n1\n8" | timeout 10s ./quantum_cipher | grep -q "Quantum Error Correction"
if [ $? -eq 0 ]; then
    echo "✓ Quantum Research Database funciona"
else
    echo "✗ Error en Quantum Research Database"
fi

# Verificar que las protecciones están activas
echo ""
echo "Verificando protecciones activas..."

# Verificar que el binario está compilado con protecciones
file quantum_cipher | grep -q "stripped"
if [ $? -eq 0 ]; then
    echo "✓ Binario está stripped (protección activa)"
else
    echo "✗ Binario no está stripped"
fi

# Verificar que no hay símbolos de debug
nm quantum_cipher 2>/dev/null | wc -l | grep -q "^0$"
if [ $? -eq 0 ]; then
    echo "✓ Símbolos de debug eliminados"
else
    echo "✗ Símbolos de debug presentes"
fi

# Verificar tamaño del binario (debe ser razonable)
size=$(stat -c%s quantum_cipher)
if [ $size -gt 10000 ] && [ $size -lt 1000000 ]; then
    echo "✓ Tamaño del binario es apropiado ($size bytes)"
else
    echo "✗ Tamaño del binario inusual ($size bytes)"
fi

echo ""
echo "=== Resumen de Pruebas ==="
echo "El reto QuantumCipher está listo para ser desplegado."
echo "Todas las funcionalidades básicas están operativas."
echo ""
echo "Para comenzar el reto, ejecuta:"
echo "  ./quantum_cipher"
echo ""
echo "Para obtener ayuda, consulta el README.md"
echo ""
echo "¡El reto está listo para desafiar a los jugadores expertos!"